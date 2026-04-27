import ast
import os
import re
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

_SYSTEM_INSTRUCTION = """You are a game designer who writes Python + Streamlit code.

When given a theme, output ONLY a single fenced ```python code block — no explanation, no prose.

The code block must follow this exact contract so it can be validated and executed automatically:
1. Define a function named run_variant() that takes no arguments.
2. run_variant() must render a complete number-guessing game using Streamlit.
3. All game state (secret number, attempts, status) must be stored in st.session_state.
4. The game must have a defined numeric range and a maximum attempt limit.
5. The game must display a win message when the player guesses correctly.
6. The game must display a loss message when attempts are exhausted.
7. Do NOT call run_variant() inside the code block — the caller does that.
8. Do NOT call st.set_page_config() — it is already set by the caller.
9. Keep the code under 60 lines."""

_USER_PROMPT_TEMPLATE = "Theme: {theme}"


_GEMINI_CONFIG = types.GenerateContentConfig(
    system_instruction=_SYSTEM_INSTRUCTION,
    temperature=0.7,
)

_RETRY_PROMPT_TEMPLATE = """The code you returned has a problem:

{error}

Here is the code you returned:
```python
{bad_code}
```

Fix the problem and return the corrected ```python code block only."""


def _call_gemini(contents: str) -> str:
    response = _client.models.generate_content(
        model="gemini-2.0-flash",
        contents=contents,
        config=_GEMINI_CONFIG,
    )
    return response.text or ""


def _extract_code(text: str) -> str | None:
    match = re.search(r"```python\n(.*?)```", text, re.DOTALL)
    return match.group(1).strip() if match else None


def _validate(code: str) -> str | None:
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return f"SyntaxError: {e}"

    has_run_variant = any(
        isinstance(node, ast.FunctionDef) and node.name == "run_variant"
        for node in ast.walk(tree)
    )
    if not has_run_variant:
        return "Missing: a function named run_variant() is not defined."

    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "run_variant"
        ):
            return "Violation: run_variant() must not be called inside the code block."

    if "st.set_page_config" in code:
        return "Violation: st.set_page_config() must not be called."

    return None


def run_agent(theme: str, max_retries: int = 3) -> str | None:
    """Generate → validate → retry loop. Returns validated code or None if all retries fail."""
    raw = _call_gemini(_USER_PROMPT_TEMPLATE.format(theme=theme))

    for _ in range(max_retries):
        code = _extract_code(raw)
        if code is None:
            error = "Your response did not contain a ```python code block."
            raw = _call_gemini(f"Theme: {theme}\n\n{error} Try again.")
            continue

        error = _validate(code)
        if error is None:
            return code

        raw = _call_gemini(_RETRY_PROMPT_TEMPLATE.format(error=error, bad_code=code))

    return None
