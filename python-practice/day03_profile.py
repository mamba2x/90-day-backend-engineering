# def greet():
#     print("HELLO WORLD")

# greet()
# greet()
# greet()

# def greet_user(name):
#     print(f"hello {name}")

# greet_user("John")

# def numbers(num1, num2):
#     return num1+num2

# result = numbers(10, 20)
# print(f"result: {result}")



# scores = [85, 90, 78, 92, 88]
# average = calculate_average(scores)
# print(f"Average score: {average:.2f}")

# practical task: Student Score Analyse
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

name = input("Enter your name: ")
scores = []
for i in range(1, 6):
    score = float(input(f"Enter score {i}: "))
    scores.append(score)
    
print(f"Average score: {calculate_average(scores):.2f}")
print(f"Highest score: {find_highest(scores):.2f}")
print(f"Lowest score: {find_lowest(scores):.2f}")
print(f"Grade: {calculate_grade(calculate_average(scores))}")
print(f"Number of Distinctions: {count_Distinction(scores)}")
print(f"Number of Failures: {count_Fail(scores)}")
