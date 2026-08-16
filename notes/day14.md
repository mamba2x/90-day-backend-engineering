# Day 14 - File Handling, Persistence and Testing

## Topic

Today I learned how to make a Python program store data permanently using file handling with `pathlib.Path`.

Previously, student information only existed while the program was running. Once the program stopped, the data was lost.

Using files allows the program to save student records and retrieve them later.

---

## 1. Using `Path`

The `Path` class is imported from Python's `pathlib` module.

```python
from pathlib import Path
```

A file can be represented using:

```python
FILE_PATH = Path("students.txt")
```

This creates a `Path` object that points to the `students.txt` file.

---

## 2. Checking if a File Exists

Before attempting to read a file, I can check whether the file exists.

```python
FILE_PATH.exists()
```

Example:

```python
if FILE_PATH.exists():
    print("File exists")
```

This prevents errors when trying to read a file that has not been created yet.

---

## 3. Reading From a File

The `read_text()` method reads the content of a text file.

```python
data = FILE_PATH.read_text(encoding="utf-8")
```

Example:

```python
if FILE_PATH.exists():
    data = FILE_PATH.read_text(encoding="utf-8")
else:
    data = ""
```

---

## 4. Writing to a File

The `write_text()` method writes text into a file.

```python
FILE_PATH.write_text(data, encoding="utf-8")
```

`write_text()` replaces the existing content, so when I want to preserve previous student records, I first read the existing content and then add the new data.

Example:

```python
existing_data = FILE_PATH.read_text(encoding="utf-8")

FILE_PATH.write_text(
    existing_data + new_data,
    encoding="utf-8"
)
```

---

## 5. Saving Student Records

Student information can be converted into text before being stored.

Example:

```python
scores = ",".join(str(score) for score in student.scores)

student_data = (
    f"{student.name}|"
    f"{student.student_id}|"
    f"{scores}\n"
)
```

This could produce:

```text
Nonso|22CD032179|78.0,65.0,82.0
```

Each student is stored on a new line.

---

## 6. Reading Saved Students

Saved student records can be read from the file.

```python
data = FILE_PATH.read_text(encoding="utf-8")
```

The records can then be separated using:

```python
data.splitlines()
```

Example:

```python
students = []

for line in data.splitlines():
    if line:
        students.append(line)
```

---

## 7. Score Validation

Each score must be between `0` and `100`.

```python
if score < 0 or score > 100:
    print("Score must be between 0 and 100")
    continue
```

The score should only be added to the list after it has passed validation.

```python
scores.append(score)
```

---

## 8. Handling Invalid Number Input

`try` and `except` are used to prevent the program from crashing if the user enters something that cannot be converted into a number.

```python
try:
    score = float(input("Enter score: "))
except ValueError:
    print("Enter a valid number")
```

---

## 9. Repeating Until Valid Input

A `while True` loop can repeatedly request the same score until valid data is entered.

```python
while True:
    try:
        score = float(input("Enter score: "))

        if score < 0 or score > 100:
            print("Score must be between 0 and 100")
            continue

        scores.append(score)
        break

    except ValueError:
        print("Enter a valid number")
```

`continue` repeats the loop.

`break` stops the loop after valid input has been received.

---

## 10. Separating Responsibilities

The Student Record Manager is separated into different files.

```text
day14/
│
├── main.py
├── student.py
├── storage.py
├── students.txt
└── test_student.py
```

### `student.py`

Contains the `Student` class and methods such as:

```text
calculate_average()
find_highest()
find_lowest()
calculate_grade()
```

### `storage.py`

Handles:

```text
Saving student records
Reading student records
Checking whether the storage file exists
```

### `main.py`

Handles:

```text
User input
Score validation
Creating Student objects
Calling storage functions
Displaying results
```

### `test_student.py`

Contains unit tests for the behaviour of the `Student` class.

---

## 11. Unit Testing

Unit tests confirm that individual parts of the program behave correctly.

Tests can verify:

```text
Average calculation
Highest score
Lowest score
Grade calculation
```

Tests can be run using:

```bash
python -m unittest
```

A successful test run should end with:

```text
OK
```

---

## Key Lesson

Today I learned that program data normally disappears when the program stops.

File persistence allows data to survive between program executions.

I also learned that different parts of an application should have separate responsibilities.

Instead of putting everything inside `main.py`:

```text
student.py -> Student behaviour

storage.py -> File handling

main.py -> Program flow

test_student.py -> Testing
```

This makes the program easier to understand, test and maintain.

---

# Day 14 Completed Checklist

* [ ] Reviewed and corrected the Student Record Manager
* [ ] Used the `Student` class from a separate module
* [ ] Collected student name and student ID from user input
* [ ] Collected multiple student scores
* [ ] Added score range validation
* [ ] Prevented invalid scores from being stored
* [ ] Handled non-numeric input with `try` and `except`
* [ ] Used a loop to repeat input until a valid score was entered
* [ ] Learned file persistence
* [ ] Used `pathlib.Path`
* [ ] Used `Path.exists()` to check whether a file exists
* [ ] Used `Path.read_text()` to read saved data
* [ ] Used `Path.write_text()` to write data
* [ ] Saved student records to `students.txt`
* [ ] Preserved previously saved student records
* [ ] Read student records back from the file
* [ ] Separated file-handling logic into `storage.py`
* [ ] Kept the `Student` class inside `student.py`
* [ ] Kept application flow inside `main.py`
* [ ] Practised unit testing
* [ ] Tested Student calculation methods
* [ ] Completed the Day 14 practical task

## Day 14 Status

**COMPLETED ✅**
