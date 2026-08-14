from pathlib import Path

reports_folder = Path("reports")

reports_folder.mkdir(exist_ok=True)

report_file = reports_folder / "student_report.txt"

report_file.write_text(
    "Student: Nonso\n"
    "Course: Software Engineering\n"
    "Grade: Distinction\n"
)

print("Report created successfully.")

