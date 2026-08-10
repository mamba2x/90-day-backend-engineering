# Day 8: Exceptions, Input Validation and Tracebacks

## What I Built

For Day 8, I improved my Student Score Manager so that it can handle invalid user input without crashing.

The program:

- Collects five student scores
- Rejects non-numeric input
- Rejects scores below 0
- Rejects scores above 100
- Keeps asking until a valid score is entered
- Calculates the average score
- Finds the highest score
- Finds the lowest score
- Counts passes
- Counts failures
- Calculates the final grade

I separated the program into `main.py` and `calculator.py`.

---

## Exceptions

An exception is an error that happens while a Python program is running.

For example, if Python tries to convert text such as `"hello"` into a number, it raises a `ValueError`.

I learned that exceptions can be handled using `try` and `except`.

Example:

```python
try:
    score = float(input("Enter score: "))
except ValueError:
    print("Enter a valid number.")

Day 8 Completion Checklist
 I understand what an exception is.
 I understand try.
 I understand except.
 I handled ValueError.
 I avoided using a bare except.
 My program rejects non-numeric input.
 My program rejects scores below 0.
 My program rejects scores above 100.
 My program keeps asking until valid input is entered.
 I created a validation function.
 I separated validation and calculation logic.
 I tested a ValueError.
 I tested a ZeroDivisionError.
 I tested a ModuleNotFoundError.
 I understand the important parts of a traceback.
 I reviewed my work with AI.
 I verified the AI suggestion myself.
 I committed and pushed Day 8 to GitHub.