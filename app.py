import builtins as _builtins
import random
from typing import Any
import streamlit as st
from logic_utils import check_guess, update_score, parse_guess, get_range_for_difficulty
from agent import run_agent

_MAX_GENERATIONS = 5

_SAFE_BUILTINS: dict[str, Any] = {
    name: getattr(_builtins, name)
    for name in (
        "abs", "bool", "dict", "enumerate", "float", "int",
        "isinstance", "len", "list", "max", "min", "print",
        "range", "round", "set", "sorted", "str", "tuple", "type", "zip",
        "Exception", "ValueError", "KeyError",
    )
}


st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}

attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "variant_code" not in st.session_state:
    st.session_state.variant_code = None

if "variant_calls" not in st.session_state:
    st.session_state.variant_calls = 0

st.sidebar.divider()
st.sidebar.subheader("AI Variant Generator")
remaining = _MAX_GENERATIONS - st.session_state.variant_calls
st.sidebar.caption(f"Generations remaining: {remaining}/{_MAX_GENERATIONS}")
theme_input = st.sidebar.text_input("Theme", placeholder="e.g. haunted house, outer space")
generate_btn = st.sidebar.button("Generate Variant", disabled=remaining <= 0)

if generate_btn:
    if not theme_input:
        st.sidebar.warning("Enter a theme first.")
    elif remaining <= 0:
        st.sidebar.error("Generation limit reached for this session.")
    else:
        with st.sidebar:
            with st.spinner("Generating..."):
                code = run_agent(theme_input)
        st.session_state.variant_calls += 1
        if code:
            st.session_state.variant_code = code
            st.rerun()
        else:
            st.sidebar.error("Could not generate a valid variant after 3 attempts. Playing default game.")

if st.session_state.variant_code:
    if st.sidebar.button("Clear Variant"):
        st.session_state.variant_code = None
        st.rerun()

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if st.session_state.variant_code:
    namespace: dict[str, Any] = {"st": st, "random": random, "__builtins__": _SAFE_BUILTINS}
    exec(st.session_state.variant_code, namespace)  # noqa: S102
    namespace["run_variant"]()
    st.stop()

st.subheader("Make a guess")

attempts_info = st.empty()

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(1, 100)
    st.session_state.status = "playing"
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)
        
        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

attempts_info.info(
    f"Guess a number between 1 and 100. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
