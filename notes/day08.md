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
```

## Day 8 Completion Checklist
- [x] I understand what an exception is.
- [x] I understand how `try` works.
- [x] I understand how `except` works.
- [x] I handled `ValueError`.
- [x] I avoided using a bare `except`.
- [x] My program rejects non-numeric input.
- [x] My program rejects scores below 0.
- [x] My program rejects scores above 100.
- [x] My program keeps asking until valid input is entered.
- [x] I created a `get_valid_score()` validation function.
- [x] I separated validation logic from the main program.
- [x] I separated calculation logic into reusable functions.
- [x] I tested a `ValueError`.
- [x] I tested a `ZeroDivisionError`.
- [x] I tested a `ModuleNotFoundError`.
- [x] I understand how to read the important parts of a traceback.
- [x] I reviewed my code with AI.
- [x] I verified the AI suggestion myself.
- [x] I fixed misleading variable and function names.
- [x] I tested my program with valid and invalid inputs.
- [x] I committed and pushed Day 8 to GitHub.
    