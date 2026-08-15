# Day 13 - Git Workflow, Branches, Commits and Merge Conflicts

## What I Learned

Today I learned how Git manages changes in a software project and how developers use branches to work safely without directly affecting the main codebase.

I also learned how to inspect changes, create commits, merge branches, resolve merge conflicts, and recover from common Git mistakes.

---

## Git Workflow

The basic Git workflow is:

```text
Working Directory
        ↓
     git add
        ↓
   Staging Area
        ↓
    git commit
        ↓
 Local Repository
        ↓
     git push
        ↓
 Remote Repository
     (GitHub)
```

A simple way to remember this is:

```text
edit → stage → commit → push
```

---

## Working Directory

The working directory contains the files I am currently editing.

When I modify a file, Git detects the change.

I can inspect the state of the project using:

```powershell
git status
```

This shows files that are:

* modified
* staged
* untracked

---

## Staging Area

The staging area contains the changes that I want to include in my next commit.

To stage one file:

```powershell
git add filename.py
```

To stage multiple changes:

```powershell
git add .
```

It is better to understand what I am staging instead of blindly using `git add .`.

---

## Commits

A commit creates a saved snapshot of staged changes in the Git repository.

Example:

```powershell
git commit -m "Add Day 13 greeting application"
```

Each commit has a unique commit hash.

---

## Inspecting Changes

To view unstaged changes:

```powershell
git diff
```

To view staged changes:

```powershell
git diff --staged
```

This allows me to inspect my code before creating a commit.

---

## Git History

To view full commit history:

```powershell
git log
```

For a cleaner history:

```powershell
git log --oneline
```

Example:

```text
918e32a Complete Day 12 filesystem practice
c202d81 Complete Day 11 OOP practice
49fe120 Complete Day 10 Python OOP
```

The short value at the beginning is part of the commit hash.

---

## Git Branches

Branches allow developers to work on features or fixes separately from the stable `main` branch.

Example:

```text
main
 │
 └── feature/day13-git-practice
```

This allows development work to happen without immediately changing `main`.

---

## Creating a Branch

I created the Day 13 feature branch using:

```powershell
git switch -c feature/day13-git-practice
```

To view branches:

```powershell
git branch
```

The `*` shows the currently active branch.

---

## Day 13 Git Application

I created:

```text
python-practice/
└── day13-git-workflow/
    └── app.py
```

The application asks the user for their name and programming language.

Example:

```python
def greet_developer(name, language):
    return f"Good afternoon {name}, please Keep building with {language}?"


name = input("enter your name: ")
language = input("enter the language you are familiar with:")

print(greet_developer(name, language))
```

I committed my work on the feature branch before merging it into `main`.

---

## Merging a Branch

After completing the feature, I switched back to the main branch:

```powershell
git switch main
```

Then merged the feature branch:

```powershell
git merge feature/day13-git-practice
```

After confirming the merge was successful, I deleted the completed feature branch:

```powershell
git branch -d feature/day13-git-practice
```

Running:

```powershell
git branch
```

confirmed that I was back on:

```text
* main
```

---

## Merge Conflicts

A merge conflict happens when Git cannot automatically decide between two conflicting changes.

This commonly happens when two branches modify the same part of the same file differently.

A conflicted file can contain:

```text
<<<<<<< HEAD
mode=production
=======
mode=testing
>>>>>>> feature/config-change
```

The markers show the conflicting versions.

The developer must choose the correct result and remove the conflict markers.

---

## Merge Conflict Lab

I created a separate Git repository for practising merge conflicts.

Initial configuration:

```text
mode=development
```

On the feature branch:

```text
mode=testing
```

On the main branch:

```text
mode=production
```

When I merged:

```powershell
git merge feature/config-change
```

Git produced:

```text
CONFLICT (content): Merge conflict in config.txt
Automatic merge failed; fix conflicts and then commit the result.
```

I manually resolved the conflict and kept:

```text
mode=production
```

Then staged the resolved file:

```powershell
git add config.txt
```

And committed the resolution:

```powershell
git commit -m "Resolve configuration merge conflict"
```

Finally:

```powershell
git status
```

returned:

```text
On branch main
nothing to commit, working tree clean
```

This confirmed that the merge conflict was successfully resolved.

---

## Git Restore

To discard unstaged changes:

```powershell
git restore filename.py
```

This removes the local changes and restores the file to its previous committed version.

This should be used carefully because the changes can be lost.

---

## Unstage a File

If I accidentally stage a file:

```powershell
git add filename.py
```

I can remove it from the staging area using:

```powershell
git restore --staged filename.py
```

This keeps my changes but removes them from the next commit.

---

## Difference Between Git Restore Commands

```powershell
git restore filename.py
```

Discards the unstaged changes.

```powershell
git restore --staged filename.py
```

Removes the file from staging while keeping the changes.

---

## Professional Git Workflow

A typical software engineering workflow looks like:

```text
main
 ↓
create feature branch
 ↓
write code
 ↓
inspect changes
 ↓
stage changes
 ↓
commit
 ↓
test
 ↓
merge into main
 ↓
delete completed branch
 ↓
push to GitHub
```

Branches allow multiple developers to work independently before combining their changes.

---

## Important Concepts

### `git add`

Moves changes into the staging area.

### `git commit`

Creates a saved snapshot of staged changes.

### `git status`

Shows the current state of the repository.

### `git diff`

Shows unstaged changes.

### `git diff --staged`

Shows staged changes.

### `git log --oneline`

Shows a simplified Git history.

### `git branch`

Shows available branches.

### `git switch`

Moves between branches.

### `git merge`

Combines changes from another branch into the current branch.

---

## Why Developers Use Branches

Branches allow developers to work on features, bug fixes, and experiments separately without immediately changing the stable main branch.

Once the work has been tested and reviewed, it can be merged into `main`.

---

# Day 13 Completed Checklist

* [x] Understand what Git version control does
* [x] Understand the working directory
* [x] Understand the staging area
* [x] Understand the local repository
* [x] Understand `edit → stage → commit`
* [x] Use `git status`
* [x] Use `git diff`
* [x] Use `git diff --staged`
* [x] Use `git log`
* [x] Use `git log --oneline`
* [x] Understand commit hashes
* [x] Understand what a Git branch represents
* [x] Use `git branch`
* [x] Create `feature/day13-git-practice`
* [x] Switch branches using `git switch`
* [x] Create the Day 13 greeting application
* [x] Make the first feature commit
* [x] Modify the application
* [x] Inspect changes before committing
* [x] Make the second feature commit
* [x] Switch back to `main`
* [x] Merge the Day 13 feature branch
* [x] Delete the merged feature branch
* [x] Confirm `main` is the active branch
* [x] Understand what causes a merge conflict
* [x] Understand Git conflict markers
* [x] Create a separate merge-conflict practice repository
* [x] Create conflicting changes on two branches
* [x] Trigger an intentional merge conflict
* [x] Manually resolve the merge conflict
* [x] Stage the resolved file
* [x] Commit the merge-conflict resolution
* [x] Confirm `working tree clean`
* [x] Understand `git restore`
* [x] Understand `git restore --staged`
* [x] Understand the basic professional feature-branch workflow
* [x] Understand why software teams use branches
* [x] Complete Day 13 Git workflow practice

## Day 13 Status

**Completed ✅**

## Key Takeaway

Git is not just about pushing code to GitHub.

Git allows me to safely track the history of my project, separate new work using branches, inspect changes before committing them, merge completed work, and resolve conflicts when different versions of code disagree.

I now understand the basic Git workflow used in real software engineering projects.
