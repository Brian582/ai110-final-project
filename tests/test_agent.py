from unittest.mock import patch
from agent import run_agent, _extract_code, _validate

_VALID_CODE = """import streamlit as st
import random

def run_variant():
    if "secret" not in st.session_state:
        st.session_state.secret = random.randint(1, 10)
    st.write("Guess a number between 1 and 10")""".strip()

_VALID_RESPONSE = f"```python\n{_VALID_CODE}\n```"


# --- _extract_code ---

def test_extract_code_returns_code_block():
    assert _extract_code(_VALID_RESPONSE) == _VALID_CODE

def test_extract_code_returns_none_when_no_block():
    assert _extract_code("Here is some text with no code block.") is None


# --- _validate ---

def test_validate_passes_valid_code():
    assert _validate(_VALID_CODE) is None

def test_validate_catches_syntax_error():
    error = _validate("def run_variant(\n    pass")
    assert error is not None
    assert "SyntaxError" in error

def test_validate_catches_missing_run_variant():
    error = _validate("def some_other_function():\n    pass")
    assert error is not None
    assert "run_variant" in error

def test_validate_catches_run_variant_call():
    code = "def run_variant():\n    pass\nrun_variant()"
    error = _validate(code)
    assert error is not None
    assert "must not be called" in error

def test_validate_catches_set_page_config():
    code = "import streamlit as st\ndef run_variant():\n    st.set_page_config()"
    error = _validate(code)
    assert error is not None
    assert "set_page_config" in error


# --- run_agent ---

def test_run_agent_returns_code_on_first_success():
    with patch("agent._call_gemini", return_value=_VALID_RESPONSE):
        result = run_agent("space")
    assert result == _VALID_CODE

def test_run_agent_retries_when_no_code_block():
    # First response lacks a code block; second is valid.
    with patch("agent._call_gemini", side_effect=["no code block here", _VALID_RESPONSE]):
        result = run_agent("space")
    assert result == _VALID_CODE

def test_run_agent_retries_when_validation_fails():
    # First response fails validation (wrong function name); second is valid.
    bad = "```python\ndef wrong_name():\n    pass\n```"
    with patch("agent._call_gemini", side_effect=[bad, _VALID_RESPONSE]):
        result = run_agent("space")
    assert result == _VALID_CODE

def test_run_agent_returns_none_when_all_retries_exhausted():
    with patch("agent._call_gemini", return_value="no code block"):
        result = run_agent("space", max_retries=3)
    assert result is None
