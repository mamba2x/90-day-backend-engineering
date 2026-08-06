# Day 4: Dictionaries and Structured Data
# student ={
#     "name": "John Doe",
#     "scores": [85, 90, 78, 92, 88],
#     "age": 20,
#     "email": "john.doe@example.com"
# }
# print(student["name"])
# print(student["scores"][3])
# print(student["age"])
# print(student["email"])

# student["level" ] = 400
# print(student["level"])
# print(student.get("height", "Not Found"))

# # loop through the dictionary
# for key, value in student.items():
#     print(f"{key}: {value}")

    # Practical task: Student Record Manager
def find_highest(scores):
    return max(scores)
def find_lowest(scores):
    return min(scores)
def calculate_average(numbers):
    return sum(numbers) / len(numbers)
def calculate_grade(average):
    if average >= 70:
        return "distinction"
    elif average >= 60:
        return "merit"
    elif average >= 50:
        return "pass"
    else:
        return "fail"
def count_Distinction(scores):
    distinction_count = 0
    for score in scores:
        if score >= 70:
            distinction_count += 1
    return distinction_count
def count_Fail(scores):
    fail_count = 0
    for score in scores:
        if score < 45:
            fail_count += 1
    return fail_count

name = input("Enter your name: ").strip()
scores = []
department = input("Enter your department: ").strip()
for i in range(1, 6):
    score = float(input(f"Enter score {i}: "))
    scores.append(score)

student_record = {
    "name": name,
    "department": department,
    "scores": scores
    }

student_record["average_score"] = calculate_average(scores)
student_record["highest_score"] = find_highest(scores)
student_record["lowest_score"]  = find_lowest(scores)
student_record["distinction_count"] = count_Distinction(scores)
student_record["fail_count"] = count_Fail(scores)
student_record["grade"] = calculate_grade(student_record["average_score"])

print("\nStudent Record:")
for key, value in student_record.items():
    print(f"{key}: {value}")