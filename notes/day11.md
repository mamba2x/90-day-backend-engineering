# Day 11: OOP Composition and Class Responsibility

## What I Learned

Today I learned how different classes can work together using **composition**.

Composition means that one object can contain or use another object.

Instead of putting every piece of information and behaviour inside one large class, I can separate responsibilities between different classes and connect their objects together.

My program used three main classes:

* `Student`
* `Course`
* `Department`

---

## Composition

Composition represents a **"has-a" relationship**.

In my program:

```text
Student HAS A Course
Course HAS A Department
```

This means a Student object stores a Course object, while a Course object stores a Department object.

The structure can be understood as:

```text
Student
   |
   └── Course
          |
          └── Department
```

---

## Department Class

The `Department` class is responsible for storing department-related information.

For example:

```python
department1 = Department(
    "Computer Science",
    "CIS"
)
```

The Department object contains information such as:

```text
department name
department code
```

This information belongs to the Department class instead of being placed directly inside the Student class.

---

## Course Class

The `Course` class stores information related to a course.

For example:

```python
course1 = Course(
    "Software Engineering",
    "CSC425",
    department1
)
```

The Course object contains:

```text
course name
course code
department
```

The `department1` value is an actual Department object.

This means the Course object is composed with a Department object.

---

## Student Class

The `Student` class stores information related to a particular student.

The Student contains:

```text
name
student ID
scores
course
```

For example:

```python
student1 = Student(
    "mamba",
    "22CD032179",
    [32, 54, 47, 96],
    course1
)
```

The `course1` value is an actual Course object.

This means the Student object is composed with a Course object.

---

## Nested Objects

Because objects contain other objects, I can access information through multiple levels.

For example:

```python
student1.course
```

accesses the student's Course object.

I can then access:

```python
student1.course.name
```

to get the course name.

I can also go another level deeper:

```python
student1.course.department
```

This gives access to the Department object associated with that course.

This can continue with:

```python
student1.course.department.name
```

My simple way of understanding this is:

```text
student
   ↓
course
   ↓
department
```

---

## Class Responsibility

I learned that each class should have a clear responsibility.

### Student Responsibility

The Student class should handle:

* Student identity
* Student scores
* Average calculation
* Highest score
* Lowest score
* Grade calculation
* Student report information

### Course Responsibility

The Course class should handle:

* Course name
* Course code
* Course information
* The department associated with the course

### Department Responsibility

The Department class should handle:

* Department name
* Department code
* Department information

This prevents the Student class from becoming responsible for everything in the application.

---

## Why Responsibility Matters

Instead of creating one large class containing:

```text
student information
course information
department information
score calculations
```

I separated these responsibilities.

This makes the code easier to:

* Understand
* Maintain
* Reuse
* Debug
* Extend

It also makes the structure of the program more similar to how real applications are organised.

---

## Shared Objects

I created multiple Student objects.

Some students can share the same Course object.

For example:

```python
student1 = Student(..., course1)

student2 = Student(..., course1)
```

Both students reference the same `course1` object.

Another student can reference a different course:

```python
student3 = Student(..., course2)
```

This showed me that different objects can reuse and share other objects.

---

## Student Report

My Student class can generate a report containing information such as:

```text
Student name
Student ID
Course
Department
Scores
Average
Highest score
Lowest score
Grade
```

Example output from my program included:

```text
student: osita
Student id: 22CD032139
course: CSC425 - Software Engineering
scores: [32, 54, 47, 96]
average: 57.25
the highest score is: 96
the lowest score is: 32
the grade: Pass
```

The report combines information from different objects while each class still keeps its own responsibility.

---

## Composition vs Inheritance

Today I focused on composition.

Composition represents:

```text
HAS-A
```

Examples:

```text
Student HAS A Course
Course HAS A Department
Car HAS AN Engine
```

Inheritance is different and represents more of an:

```text
IS-A
```

relationship.

For example:

```text
Manager IS AN Employee
Dog IS AN Animal
```

I do not need to go deep into inheritance yet.

---

## Important Lesson

Creating many classes does not automatically mean the program has good OOP design.

The important thing is that each class has a sensible responsibility and that related objects work together.

My simple rule is:

> A class should be responsible for the information and behaviour that logically belongs to it.

---

## Interview Question

### What is composition in Object-Oriented Programming?

Composition is when one object contains or uses another object.

It represents a **"has-a" relationship**.

For example:

```text
Student HAS A Course.
Course HAS A Department.
```

### Why is composition useful?

Composition allows responsibilities to be separated between different classes.

Instead of placing all data and behaviour inside one large class, different objects can handle their own responsibilities and work together.

---

## AI Verification Exercise

### Student Responsibility

The Student class is responsible for storing student information, scores, and calculating student results.

### Course Responsibility

The Course class is responsible for storing course information and connecting a course to its department.

### Department Responsibility

The Department class is responsible for storing department-related information.

### Where Composition Is Used

Composition is used when:

```text
Student contains a Course object.
Course contains a Department object.
```

### Was the Separation Appropriate?

Yes.

Student, Course, and Department represent different concepts and each class has its own responsibility.

Keeping them separate makes the program easier to understand and maintain.

### My Understanding

Composition allows objects to cooperate without forcing one class to contain every responsibility in the application.

---

## Day 11 Completion Checklist

* [x] I understand what composition means.
* [x] I understand a "has-a" relationship.
* [x] I understand the idea of class responsibility.
* [x] I understand why one class should not handle every responsibility.
* [x] I created a `Department` class.
* [x] I created a `Course` class.
* [x] I created a `Student` class.
* [x] My Department stores department information.
* [x] My Department stores a department name.
* [x] My Department stores a department code.
* [x] My Course stores course information.
* [x] My Course stores a course name.
* [x] My Course stores a course code.
* [x] My Course stores a Department object.
* [x] My Student stores student information.
* [x] My Student stores a name.
* [x] My Student stores a student ID.
* [x] My Student stores scores.
* [x] My Student stores a Course object.
* [x] I understand that the Course value is an object and not just a string.
* [x] I understand that the Department value is an object and not just a string.
* [x] I used composition between Student and Course.
* [x] I used composition between Course and Department.
* [x] I understand nested object access.
* [x] I understand `student.course`.
* [x] I understand `student.course.department`.
* [x] I calculated a student's average.
* [x] I calculated the highest score.
* [x] I calculated the lowest score.
* [x] I calculated the student's grade.
* [x] I generated student reports.
* [x] I created multiple Student objects.
* [x] I created multiple Course objects.
* [x] I created multiple Department objects.
* [x] I reused Course objects between students.
* [x] I connected different students to different courses.
* [x] I displayed course information in the student report.
* [x] I displayed department information in the student report.
* [x] I understand why Course information belongs to Course.
* [x] I understand why Department information belongs to Department.
* [x] I understand why Student should not contain every responsibility.
* [x] I understand the basic difference between composition and inheritance.
* [x] I can explain composition in my own words.
* [x] I can explain class responsibility in my own words.
* [x] I can answer the interview question about composition.
* [x] My Day 11 program runs successfully.
* [x] I completed my Day 11 practical task.
* [x] I completed my Day 11 notes.
* [x] I completed Day 11.
