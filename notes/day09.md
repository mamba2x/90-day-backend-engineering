# Day 9: Python Testing Fundamentals

## What I Learned

Today I learned the basics of automated testing in Python using the `unittest` module.

Automated testing allows me to verify that my functions behave correctly without manually running the whole application every time.

I learned that a test compares the actual result of my code with the result I expect.

---

## unittest

I used Python's built-in `unittest` framework.

My test class inherits from:

`unittest.TestCase`

This gives me access to testing methods such as:

`self.assertEqual()`

Example:

```python
result = calculator.calculate_average([70, 60, 80])
self.assertEqual(result, 70)
```

## Day 9 Completion Checklist

- [x] I understand why automated tests are useful.
- [x] I understand what a test case is.
- [x] I understand what an assertion does.
- [x] I created `test_calculator.py`.
- [x] I used Python's `unittest` framework.
- [x] I created a class that inherits from `unittest.TestCase`.
- [x] I used `self.assertEqual()`.
- [x] I tested `calculate_average()`.
- [x] I tested `find_highest()`.
- [x] I tested `find_lowest()`.
- [x] I tested the pass-counting function.
- [x] I tested the fail-counting function.
- [x] I tested `calculate_grade()`.
- [x] I tested normal scores.
- [x] I tested all-pass scores.
- [x] I tested all-fail scores.
- [x] I tested mixed pass and fail scores.
- [x] I tested the grade boundary at 50.
- [x] I tested the grade boundary at 60.
- [x] I tested the grade boundary at 70.
- [x] I wrote at least 10 tests.
- [x] I made sure my test methods start with `test_`.
- [x] I deliberately introduced a bug.
- [x] I saw the test suite catch the bug.
- [x] I fixed the bug and confirmed all tests passed again.
- [x] I reviewed my tests with AI.
- [x] I verified the AI suggestions myself.
- [x] I ran my tests successfully.
- [x] I committed and pushed Day 9 to GitHub.