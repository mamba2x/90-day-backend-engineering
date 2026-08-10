def get_valid_scores(number):
    while True:
        try:
            score= int(input(f"enter user scores {number}:"))
            if score<0 or score>100:
                print("enter scores from the range of (0-100)")
                continue
            return score
        except ValueError:
            print("enter valid numbers")

def calculate_average(numbers):
    return sum(numbers) / len(numbers)

def calculate_highest(numbers):
    return max(numbers)

def calculate_lowest(numbers):
    return min(numbers)

def number_of_passes(numbers):
    pass_count = 0
    for score in numbers:
        if score >= 50:
            pass_count += 1
    return pass_count

def number_of_fails(numbers):
    fail_count = 0
    for score in numbers:
        if score < 50:
            fail_count += 1
    return fail_count

def calculate_grade(average):
    if average >= 70:
        return "distinction"
    elif average >=60:
        return "Merit"
    elif average >=50:
        return "pass"
    elif average < 50:
        return "fail"