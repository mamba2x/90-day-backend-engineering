from pathlib import Path


FILE_PATH = Path("students.txt")


def save_student(student):
    scores = ",".join(str(score) for score in student.scores)

    student_data = (
        f"{student.name}|"
        f"{student.student_id}|"
        f"{scores}\n"
    )

    if FILE_PATH.exists():
        existing_data = FILE_PATH.read_text(encoding="utf-8")
    else:
        existing_data = ""

    FILE_PATH.write_text(
        existing_data + student_data,
        encoding="utf-8"
    )


def read_students():
    if not FILE_PATH.exists():
        return []

    data = FILE_PATH.read_text(encoding="utf-8")

    students = []

    for line in data.splitlines():
        if line:
            students.append(line)

    return students