import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

_SYSTEM_PROMPT = """You are a game designer. Given a theme, generate a Python + Streamlit
number-guessing game variant as a single self-contained code block.

Rules:
- Output only a fenced ```python code block, nothing else.
- The code must define a function called run_variant() that renders the full game using Streamlit.
- The code must not call run_variant() itself — the caller will do that.
- The code must not use st.set_page_config().
- Keep it under 60 lines."""


def generate_variant(theme: str) -> str:
    """Call Gemini once with the given theme and return the raw response text."""
    prompt = f"{_SYSTEM_PROMPT}\n\nTheme: {theme}"
    response = _client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    return response.text
