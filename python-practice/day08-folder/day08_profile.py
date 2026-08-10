# without try and exception handler these program crashes when the user input unexpected values
age = int(input("enter your age"))
print(f"the use age is: {age}")

# using the Try and exception handler 

try:
    score= float(input("enter your scores"))
    if score <0 or score > 100:
        print("enter score less than 100 and greater than 0")
except ValueError:
        print("please enter a valid value")
def get_score():
    while True:
        try:
            scores= int(input("enter user scores"))
            if scores<0 or scores>100:
                print("enter scores from the range of (0-100)")
                continue
            return scores
        except ValueError:
            print("enter valid numbers")

score_value = get_score()
print(score_value)

