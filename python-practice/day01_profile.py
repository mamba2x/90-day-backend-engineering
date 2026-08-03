# variables and data types
name = "Daddy"
age = 22
height = 1.82
is_student = True

print("Name:", name)
print(name, "is learning python.")
print(f"{name} is learning Python")

name_1= input("Enter your name: ")    
print("Hello", name_1, "Welcome to Python programming!")    
age= int(input("Enter your age: "))

# Arithmetic operations
num1 = 10
num2 = 5
sum_result = num1 + num2
multiplication_result = num1 * num2
division_result = num1 / num2
subtraction_result = num1 - num2
print("Sum:", sum_result)
print("Multiplication:", multiplication_result)
print("Division:", division_result)
print("Subtraction:", subtraction_result)


# Practical Task
student_name = input("Enter your name: ")
first_score = float(input("Enter your first score: "))
second_score = float(input("Enter your second score: "))
third_score = float(input("Enter your third score: "))
average_score = (first_score + second_score + third_score) / 3
print(f"the Average score of student is {average_score}")

if average_score >= 70:
    grade = "Distinction"
elif average_score >= 60:
    grade = "Merit"
elif average_score >= 50:
    grade = "Pass"
else:
    grade = "Fail"


print("========================")
print(f"student: {student_name}")
print(f"average score: {average_score:.2f}")
print(f"grade: {grade}")
    