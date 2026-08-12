# Day 10: Object-Oriented Programming Basics

## What I Learned

Today I learned the basics of Object-Oriented Programming (OOP) in Python.

OOP allows me to organise related data and behaviour inside classes.

Instead of keeping student information and functions separately, I can create a `Student` class that contains both the student's data and the methods that operate on that data.

---

## Classes and Objects

A **class** is a blueprint that defines what an object should contain and what it should be able to do.

Example:

```python
class Student:
    pass
```

An **object** is a specific instance created from a class.

Example:

```python
student1 = Student()
```

I learned that multiple objects can be created from the same class, and each object can store different data.

---

## The `__init__` Method

The `__init__` method runs automatically when a new object is created.

Example:

```python
class Student:

    def __init__(self, name, scores, student_id):
        self.name = name
        self.scores = scores
        self.student_id = student_id
```

Then I can create an object like:

```python
student1 = Student(
    "Nonso",
    [78, 32, 68],
    "22CD032179"
)
```

The values are stored inside that particular student object.

---

## Attributes

Attributes are values that belong to an object.

For my `Student` class, the attributes are:

```python
self.name
self.scores
self.student_id
```

For example:

```python
print(student1.name)
print(student1.student_id)
```

---

## Methods

A method is a function that belongs to a class.

Example:

```python
def find_highest(self):
    return max(self.scores)
```

I can call it using:

```python
student1.find_highest()
```

I learned that:

```python
student1.find_highest
```

refers to the method itself, while:

```python
student1.find_highest()
```

actually executes the method and returns its result.

---

## Understanding `self`

`self` refers to the particular object currently using a method.

For example:

```python
student1.calculate_grade()
```

When this runs:

```python
def calculate_grade(self):
```

`self` refers to `student1`.

Therefore:

```python
self.calculate_average()
```

means that Python should calculate the average belonging to that particular student.

If another object calls the same method:

```python
student2.calculate_grade()
```

then `self` refers to `student2`.

This allows the same class and methods to work with many different objects while each object keeps its own data.

My simple way of remembering it is:

> `self` means "this particular object."

---

## Calling One Method From Another Method

I learned that methods inside a class can call other methods belonging to the same object.

Example:

```python
def calculate_grade(self):
    average = self.calculate_average()

    if average >= 70:
        return "Distinction"
    elif average >= 60:
        return "Merit"
    elif average >= 50:
        return "Pass"
    else:
        return "Fail"
```

Instead of calculating the average again, `calculate_grade()` reuses the existing `calculate_average()` method.

---

## Student Class

My Student class contains methods for:

* Finding the highest score
* Finding the lowest score
* Calculating the average
* Calculating the grade
* Displaying a student report

Example structure:

```python
class Student:

    def __init__(self, name, scores, student_id):
        self.name = name
        self.scores = scores
        self.student_id = student_id

    def find_highest(self):
        return max(self.scores)

    def find_lowest(self):
        return min(self.scores)

    def calculate_average(self):
        return sum(self.scores) / len(self.scores)

    def calculate_grade(self):
        average = self.calculate_average()

        if average >= 70:
            return "Distinction"
        elif average >= 60:
            return "Merit"
        elif average >= 50:
            return "Pass"
        else:
            return "Fail"

    def display_report(self):
        print(f"Student: {self.name}")
        print(f"Student ID: {self.student_id}")
        print(f"Average: {self.calculate_average():.2f}")
        print(f"Highest: {self.find_highest()}")
        print(f"Lowest: {self.find_lowest()}")
        print(f"Grade: {self.calculate_grade()}")
```

---

## Errors I Encountered

### Incorrect `__init__`

The constructor must be written with double underscores:

```python
def __init__(self, name, scores, student_id):
```

---

### Forgetting Parentheses When Calling Methods

Incorrect:

```python
highest_score = student1.find_highest
```

Correct:

```python
highest_score = student1.find_highest()
```

Without the parentheses, Python gives me the method itself instead of executing it.

---

### Forgetting `self` in a Method

Incorrect:

```python
def calculate_grade(average):
```

Correct:

```python
def calculate_grade(self):
```

The method needs `self` so it knows which Student object is currently using it.

---

## OOP Example

```python
student1 = Student(
    "Nonso",
    [78, 32, 68],
    "22CD032179"
)

student1.display_report()
```

For these scores:

```text
78, 32, 68
```

the average is approximately:

```text
59.33
```

Therefore the final grade is:

```text
Pass
```

---

## Interview Question

### What is the difference between a class and an object?

A class is a blueprint that defines the attributes and behaviours something should have.

An object is a specific instance created from that class.

Example:

```python
class Student:
```

defines the class.

While:

```python
student1 = Student("Nonso", [78, 32, 68], "22CD032179")
```

creates an object.

### What is `self` in Python?

`self` refers to the current instance of a class.

It allows methods to access or modify the attributes belonging to the particular object currently using the method.

---

## Day 10 Completion Checklist

* [x] I understand the basic idea of Object-Oriented Programming.
* [x] I understand what a class is.
* [x] I understand what an object is.
* [x] I understand the difference between a class and an object.
* [x] I understand what `__init__` does.
* [x] I understand what `self` means.
* [x] I understand that `self` refers to the current object.
* [x] I understand what an attribute is.
* [x] I understand what a method is.
* [x] I created my own `Student` class.
* [x] I created `name`, `scores`, and `student_id` attributes.
* [x] I created a `find_highest()` method.
* [x] I created a `find_lowest()` method.
* [x] I created a `calculate_average()` method.
* [x] I created a `calculate_grade()` method.
* [x] I created a `display_report()` method.
* [x] I understand how one method can call another using `self`.
* [x] I understand the difference between `student1.find_highest` and `student1.find_highest()`.
* [x] I fixed errors involving missing method parentheses.
* [x] I fixed errors involving `self`.
* [x] I fixed my `__init__` method.
* [x] I successfully created a Student object.
* [x] I accessed object attributes using dot notation.
* [x] I called methods using dot notation.
* [x] I calculated a student's average using an object method.
* [x] I calculated a student's highest and lowest scores.
* [x] I calculated a student's grade.
* [x] I understand that different objects can store different data.
* [x] I can explain `self` in my own words.
* [x] I can explain the difference between a class and an object.
* [x] My Day 10 Student program runs successfully.
* [x] I completed my Day 10 notes.
* [x] I completed Day 10.
