import os
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


def generate_variant(theme: str) -> str:
    """Call Gemini once with the given theme and return the raw response text."""
    response = _client.models.generate_content(
        model="gemini-2.0-flash",
        contents=_USER_PROMPT_TEMPLATE.format(theme=theme),
        config=types.GenerateContentConfig(
            system_instruction=_SYSTEM_INSTRUCTION,
            temperature=0.7,
        ),
    )
    return response.text or ""
