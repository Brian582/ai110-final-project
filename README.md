# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [ ] Describe the game's purpose.
- [ ] Detail which bugs you found.
- [ ] Explain what fixes you applied.

The point of the game is to guess the correct number in the limited number of attempts you are given. If you guess correctly you win, if you run out of attempts you lose. The bugs I found in the game were that it gave me wrong hints, it displayed the "Out of attempts" message too early, and the game didnt reset when you clicked the "New game" button. I used Claude to fix the bugs. 
"New game" button bug fix: To fix this bug, Claude added " st.session_state.status = "playing" ", so the game could properly reset when the "New game" button was clicked.
"Out of attempts" message bug fix: To fix this bug, Claude changed "attempts" initialization from 1 to 0 and put the "st.info" code near the bottom of the app.py file, so it displays the attempt count correctly.
Hint bug fix: To fix this bug, Claude swapped the hints messages and removed the code where "Secret" became a string on even attempts.



## 📸 Demo

- ![Alt text](screenshot\Screenshot.png)


## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]


## Part 3. Documentation: How You Explain Your Work

1. This project was originally the "Game Glitch Investigator" project. The project was originally used for practice for how to debug code with AI.

## Title and Summary

**Game Glitch Investigator — AI Variant Generator**

This project started as a broken Streamlit number-guessing game that students debug and fix. The new feature adds an **Agentic Workflow** powered by the Gemini API: the user types a theme (e.g. "haunted house"), and an AI agent generates a brand-new themed number-guessing game variant on the spot, validates that the code is safe and correct, and renders it inside the same app — no manual coding required.

This matters because it demonstrates a real agentic pattern: the AI doesn't just generate output once and stop. It evaluates its own result, identifies failures, and retries with corrections — the same loop used in production AI systems.

---

## Architecture Overview

The system has four main layers:

- **User (Input):** The user enters a theme and a number guess through the Streamlit sidebar and main UI.
- **Agent (`agent.py`):** Acts as both the generator and evaluator. It sends the theme to Gemini (`gemini-2.0-flash`), extracts the returned code block, and validates it using Python's `ast` module — checking for syntax errors, a required `run_variant()` function, and contract violations. If validation fails, it feeds the specific error back to Gemini and retries up to 3 times.
- **App (`app.py`):** Orchestrates everything. It enforces a 5-generation-per-session rate limit, passes the validated code into a restricted `exec` sandbox (blocking dangerous built-ins like `open` and `__import__`), and renders the result. If all retries fail, it falls back to the default game.
- **Testing:** `test_agent.py` mocks the Gemini API and tests every path through the agent loop — first-try success, retry after missing code block, retry after validation failure, and full fallback. `test_game_logic.py` covers the core game logic independently.

---

## Setup Instructions

1. **Clone the repo and create a virtual environment:**
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   pip install google-genai python-dotenv
   ```

3. **Add your Gemini API key** — create a `.env` file in the project root:
   ```
   GEMINI_API_KEY=your_key_here
   ```
   Get a free key at [aistudio.google.com](https://aistudio.google.com).

4. **Run the app:**
   ```
   streamlit run app.py
   ```

5. **Run the tests:**
   ```
   pytest
   ```

6. **Use the AI Variant Generator** — in the sidebar, type a theme (e.g. `pirates`, `outer space`) and click **Generate Variant**. The agent will generate, validate, and render a themed game. Click **Clear Variant** to return to the default game.

---

## Sample Interactions

**Example 1 — Theme: `haunted house`**
> Input: User types "haunted house" and clicks Generate Variant.
> Output: Gemini generates a game titled something like "Whispers from the beyond speak of a number between 1 and 13. You have 5 attempts to reveal its secret before the spirits claim you! What number haunts this house?"

**Example 2 — Theme: `outer space`**
> Input: User types "outer space" and clicks Generate Variant.
> Output: Gemini generates a game like " I'm thinking of a number between 1 and 100.,  Warp Jumps remaining: 7, Enter your guess for the Cosmic Code!" HINT: 1 Too low! Your trajectory needs adjusting."

---

## Design Decisions

**Why `exec` instead of saving the file and importing it?**
Using `exec` with a restricted namespace keeps the generated code sandboxed and temporary. Writing it to a `.py` file and importing it would leave files on disk, require managing module cache (`importlib.reload`), and give the code full import access. The trade-off is that `exec` is harder to debug, but for a short-lived game variant it is the right call.

**Why AST validation instead of just running the code and catching errors?**
Running untrusted code to see if it crashes is itself a security risk — the code could do damage before it errors. Validating with `ast.parse` and `ast.walk` checks the structure without executing anything, so violations are caught safely before the sandbox ever opens.

**Why does Agentic Workflow have 3 retries and the app only has 5 generations?**
3 retries balances giving Gemini enough chances to self-correct without burning too many free-tier API calls per generation attempt. 5 generations per session is a conservative cap — worst case that is 15 API calls in one session, well within free-tier daily limits. Both numbers are constants that are easy to change.

**Trade-off: no persistent rate limiting.**
The generation counter lives in `st.session_state`, so it resets on page refresh. A real production system would track usage server-side or with a database. For a demo project this is acceptable — the cap exists to prevent accidental runaway usage, not to enforce strict quotas.

---

## Testing Summary

**What worked:**
All 11 tests pass. Mocking `_call_gemini` with `unittest.mock.patch` made it possible to test every path through the agent loop — success, retry, and fallback — without making a single real API call. The AST-based validator tests were straightforward because `_validate` is a pure function with no side effects.

**What didn't work initially:**
The `exec` sandbox broke at runtime because Gemini's generated code included `import streamlit as st` and `import random` even after being told not to. Python uses `__import__` internally to handle those statements, and `__import__` was blocked by `_SAFE_BUILTINS`. This was fixed by stripping import lines before `exec` as a safety net, and updating the system prompt to explicitly tell Gemini not to use import statements.


---

## Part 4. Reliability and Evaluation: How You Test and Improve Your AI

## Automated Tests

11/11 passed. Here is what Claude tested and what each group covered:

_extract_code (2 tests) — confirms the regex correctly pulls the fenced block, and returns None when there's no block at all.

_validate (5 tests) — one test per contract rule: valid code passes, syntax errors are caught, missing run_variant is caught, a run_variant() call at module level is caught, and st.set_page_config is caught.

run_agent (4 tests) — all mocked with patch("agent._call_gemini") so no real API calls are made: success on first try, retry after missing code block, retry after failed validation, and None returned when all retries are exhausted.

