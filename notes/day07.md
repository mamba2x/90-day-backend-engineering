# Day 7: Python Foundations Review

## What I Built

For Day 7, I created a modular Student Score Manager.

The project contains:

- `main.py` for collecting student scores and displaying results.
- `calculator.py` for reusable calculation functions.
- `requirements.txt` for recording project dependencies.
- `.gitignore` for preventing unnecessary files such as the virtual environment from being pushed to GitHub.

The program collects five scores and calculates:

- Average score
- Highest score
- Lowest score
- Number of passes
- Number of failures
- Final grade

---

## Python Modules

I separated my program into `main.py` and `calculator.py`.

`calculator.py` contains the calculation functions while `main.py` handles user input and displays the results.

I understand that using modules helps keep code organised and allows functions to be reused without copying the same code into different files.

---

## Virtual Environment

A virtual environment creates an isolated Python environment for a project.

This allows each project to have its own packages and package versions without affecting other Python projects on my computer.

I created and activated a virtual environment for this project before installing its dependencies.

---

## requirements.txt

`requirements.txt` keeps a record of the Python packages required by my project.

I generated it using:

`python -m pip freeze > requirements.txt`

I understand that `pip freeze` lists the packages installed in my current environment together with their versions.

Another developer can recreate the dependencies using:

`python -m pip install -r requirements.txt`

---

## .gitignore

I used `.gitignore` so that files and folders that should not be stored in GitHub are ignored.

My ignored files include:

- `.venv/`
- `test_env/`
- `__pycache__/`

The virtual environment should not be pushed because it contains many generated files and can be recreated using `requirements.txt`.

---

## Debugging Exercise

I deliberately tested an incorrect module import.

If my file is called:

`calculator.py`

but I try to import:

`calculators`

Python produces a `ModuleNotFoundError`.

This taught me that the name used in an import must match the module that Python can actually find.

I also learned that error messages should be read carefully because they usually provide information about what went wrong.

---

## Environment Questions

### 1. What is a virtual environment?

It is an isolated Python environment used to keep one project's packages separate from other projects.

### 2. Why do we use requirements.txt?

It records the packages a project needs so that the same dependencies can be installed in another environment.

### 3. What does pip freeze do?

It displays the packages installed in the current environment and their versions.

### 4. What does pip install -r requirements.txt do?

It reads the packages listed inside `requirements.txt` and installs them into the current Python environment.

### 5. Why should .venv not be pushed to GitHub?

The virtual environment contains generated package files and can become very large. It can be recreated from `requirements.txt`, so there is no need to store it in the repository.

---

## AI Review

### AI Claim

The AI identified that `package_name==0.1` in my `requirements.txt` may be an accidental dependency because my program does not use it.

### How I Verified It

I checked whether the package was installed and checked my Python files to see whether I imported or used it.

### Result

I confirmed whether the package was actually required by my project before deciding whether to keep or remove it.

### What I Learned

AI suggestions should not automatically be accepted. I should inspect my project and verify the claim myself before making a change.

---

## Day 7 Completion Checklist

- [x] I created a modular student report program.
- [x] I separated calculation logic into `calculator.py`.
- [x] I used functions.
- [x] I imported a Python module.
- [x] I created and activated a virtual environment.
- [x] I installed `requests`.
- [x] I generated `requirements.txt`.
- [x] I understand what `pip freeze` does.
- [x] I understand what `pip install -r requirements.txt` does.
- [x] I created `.gitignore`.
- [x] My `.venv` is not being pushed to GitHub.
- [x] I investigated an import error.
- [x] I reviewed my project with AI.
- [x] I verified an AI suggestion myself.
- [x] I committed and pushed Day 7 to GitHub.

## Self Assessment

Python logic: 26/ 30

Virtual environment: 24 / 25

Git and `.gitignore`: 18 / 20

Debugging: 11 / 15

Explanation: 9 / 10

**Total: 88 / 100**