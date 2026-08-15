# Day 12 - Command Line and Filesystem Basics

## What I Learned

Today I learned how developers interact with the filesystem using the terminal and Python.

The filesystem can be viewed as a tree made up of folders and files. The directory where the terminal is currently operating is called the **current working directory**.

## PowerShell Commands

### Check Current Directory

```powershell
pwd
```

This shows the directory I am currently inside.

### List Files and Folders

```powershell
dir
```

PowerShell also supports:

```powershell
ls
```

### Enter a Directory

```powershell
cd python-practice
```

### Go Back One Directory

```powershell
cd ..
```

`..` represents the **parent directory**.

---

## Absolute and Relative Paths

### Absolute Path

An absolute path gives the complete location of a file or folder.

Example:

```text
C:\Users\Chiso\Desktop\Among_Us\90-day-backend-engineering\python-practice
```

### Relative Path

A relative path gives the location of a file or folder based on the directory I am currently inside.

Example:

```text
python-practice\day11-folder
```

A simple way to remember this is:

```text
absolute = full address

relative = directions from where I currently am
```

---

## Creating Directories and Files

Create a new directory:

```powershell
mkdir day12-filesystem
```

Enter the directory:

```powershell
cd day12-filesystem
```

Create an empty file:

```powershell
New-Item notes.txt
```

PowerShell shorthand:

```powershell
ni notes.txt
```

---

## Moving and Renaming Files

Rename a file:

```powershell
Rename-Item notes.txt developer_notes.txt
```

Move a file:

```powershell
Move-Item developer_notes.txt archive
```

Delete a file:

```powershell
Remove-Item developer_notes.txt
```

Delete a directory and its contents:

```powershell
Remove-Item archive -Recurse
```

Deletion commands should be used carefully because terminal commands can delete files very quickly.

I should always understand a destructive command before running it.

---

## Working With the Filesystem in Python

Python provides the `pathlib` module for working with filesystem paths.

Import `Path`:

```python
from pathlib import Path
```

### Current Working Directory

```python
from pathlib import Path

current_directory = Path.cwd()

print(current_directory)
```

`Path.cwd()` returns the current working directory.

---

## Using Path Objects

Instead of representing paths only as strings:

```python
folder = "C:\\Users\\Chiso\\Desktop\\project"
```

I can create a `Path` object:

```python
from pathlib import Path

project = Path("python-practice")
```

`project` is now a `Path` object.

Because `Path` is an object, I can use methods and attributes such as:

```python
project.exists()
project.is_dir()
project.name
```

### `project.exists()`

Checks whether the path exists.

```python
project.exists()
```

### `project.is_dir()`

Checks whether the path is a directory.

```python
project.is_dir()
```

### `project.name`

Returns the name of the file or directory represented by the path.

```python
project.name
```

---

## Why This Matters

Backend development constantly involves commands such as:

```powershell
python manage.py runserver
git status
pip install ...
cd project
mkdir logs
```

Understanding the terminal and filesystem will make it easier to work with:

* Python
* Django
* Git
* Docker
* Servers
* Deployment
* Backend projects

---

## Day 12 Completed Checklist

* [x] Understand how the filesystem is structured
* [x] Understand folders and files as a filesystem tree
* [x] Understand the current working directory
* [x] Learn how to use `pwd`
* [x] Learn how to use `dir`
* [x] Learn how to use `ls`
* [x] Learn how to navigate directories using `cd`
* [x] Learn how to return to the parent directory using `cd ..`
* [x] Understand what `..` means
* [x] Understand absolute paths
* [x] Understand relative paths
* [x] Create directories using `mkdir`
* [x] Create files using `New-Item`
* [x] Use the `ni` PowerShell shortcut
* [x] Rename files using `Rename-Item`
* [x] Move files using `Move-Item`
* [x] Delete files using `Remove-Item`
* [x] Delete directories using `Remove-Item -Recurse`
* [x] Understand the danger of destructive terminal commands
* [x] Learn about Python's `pathlib` module
* [x] Import `Path` from `pathlib`
* [x] Use `Path.cwd()`
* [x] Create a `Path` object
* [x] Use `Path.exists()`
* [x] Use `Path.is_dir()`
* [x] Use `Path.name`
* [x] Understand why filesystem knowledge is important for backend development

## Day 12 Status

**Completed ✅**
