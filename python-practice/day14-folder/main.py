from student import Student
from storage import save_student, read_students


name = input("Enter your name: ")
student_id = input("Enter your student ID: ")

scores = []

for i in range(1, 4):
    while True:
        try:
            score = float(input(f"Enter score {i}: "))

            if score < 0 or score > 100:
                print("Score must be between 0 and 100")
                continue

            scores.append(score)
            break

        except ValueError:
            print("Enter a valid number")


student1 = Student(name, scores, student_id)

save_student(student1)


print("\nStudent Information")
print("-------------------")
print(f"Name: {student1.name}")
print(f"Student ID: {student1.student_id}")
print(f"Scores: {student1.scores}")
print(f"Average: {student1.calculate_average():.2f}")
print(f"Highest Score: {student1.find_highest()}")
print(f"Lowest Score: {student1.find_lowest()}")
print(f"Grade: {student1.calculate_grade()}")


print("\nSaved Students")
print("--------------")

students = read_students()

for student in students:
    print(student)