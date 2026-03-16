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
