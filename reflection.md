# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

---
When I started playing the game, I used the number 5. As I was playing the game, it started giving me wrong output.
Bug 1: The game gave me wrong hints. It kept saying to go lower, even though the secret number was 58 and that's higher than 5.
Bug 2: I got a message saying I ran out of attempts, even though the game said I have 1-2 more attempts.
Bug 3: When I click the "New game" button, the game doesnt reset.

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---
I used Claude Code for this project. 
A correct AI suggestion I got was when I was fixing the bug for getting wrong hints. Claude that 2 issues was causing this; The hint messages were swapped and Secret was cast to string on even attempts. I verified these results by letting Claude add the code it suggested to fix the bug and then I played the game again to see if the hint bug was fixed and it was. 
During this project, I didnt get an incorrect or mislead suggestion from Claude. So far, everything it explained/suggested made sense or work.

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---
I decided a bug was really fixed by either I playing the game again or using pytest. For example, I used pytest to see if I fixed the bug about the "Out of attempts" message being displayed to early. Claude helped me create the pytest function and explain how pytest was used to test parts of the code. When I ran the pytest, it said that 3 tests failed and 1 test passed which was the pytest function Claude generated. This was how I saw that the bug was fixed. I also used Claude to fix the other pytest functions. It added another variable to unpack the tuple returned by the check_guess function.


## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---
Streamlit reruns are when the entire Python file re-executes its code whenever a user interacts with a UI in the browser or when the source code changes.

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One strategy I would reuse from this project is I would use AI help me debug code when I take too long to fix it myself.
The next time I work with AI is I would ask it to explain the functions it uses, the ones I'm not familiar with.