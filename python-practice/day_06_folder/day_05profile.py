import day_05calculator
import requests
import sys
# another way to import the add function from the calculator module
# from day_05calculator import add
# result = add(5, 3)

# print(day_05calculator.add(5, 3))  
# print(day_05calculator.subtract(10, 4))  
# print(day_05calculator.multiply(6, 7))  
def main():

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
    highest_score = day_05calculator.find_highest(scores)
    lowest_score = day_05calculator.find_lowest(scores)
    average_score = day_05calculator.calculate_average(scores)
    grade = day_05calculator.calculate_grade(average_score)
    distinction_count = day_05calculator.count_Distinction(scores)
    fail_count = day_05calculator.count_Fail(scores)

    student_record["average_score"] = average_score
    student_record["highest_score"] = highest_score
    student_record["lowest_score"]  = lowest_score
    student_record["grade"] = grade
    student_record["distinction_count"] = distinction_count
    student_record["fail_count"] = fail_count

    for key, value in student_record.items():
        print(f"{key}: {value}")
    print("request imported successfully")
    print(f"requests version: {requests.__version__}")
    print(f"python version: {sys.version}")
        
if __name__ == "__main__":
    main()