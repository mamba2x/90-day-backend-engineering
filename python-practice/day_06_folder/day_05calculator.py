# def add(a, b):
#     return a + b
# def subtract(a, b):
#     return a - b
# def multiply(a,b):
#     return a*b

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