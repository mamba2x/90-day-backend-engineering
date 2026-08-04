# score_one= [12,23,32,45]
# score_two= [12,23,32,45]
# score_three= [12,23,32,45]
# score_four= [12,23,32,45]

# print(score_one[0])
# print(score_two[1])
# print(score_one.append(90))
# print(score_one.remove(32))

# print(max(score_one))
# print(min(score_one))
# print(sum(score_one))
# print(len(score_one))

# # loops
# for score in score_one:
#     print(score)

# for score in score_two:
#     if score > 20:
#         print(f"score greater than 20: {score}")
#     elif score >10:
#         print(f"score greater than 10: {score}")
#     else:
#         print(f"score less than or equal to 10: {score}")   

# for number in range(5):
#     print(f"number: {number}")


# arrays
# score_list = []

# for score_lists in range(1,4):
#     user_input = int(input(f"Enter your score:{score_lists} "))
#     score_list.append(user_input)
#     print(f"score list: {score_list}")

# temperatures = []

# for day in range(1, 6):
#     temperature = float(input(f"Enter temperature for day {day}: "))
#     temperatures.append(temperature)

# average_temperature = sum(temperatures) / len(temperatures)
# highest_temperature = max(temperatures)
# lowest_temperature = min(temperatures)

# print("\n===== TEMPERATURE REPORT =====")
# print(f"Temperatures: {temperatures}")
# print(f"Average: {average_temperature:.2f}")
# print(f"Highest: {highest_temperature:.2f}")
# print(f"Lowest: {lowest_temperature:.2f}")

# Practical task: Student Score Analyse
name = input("Enter your name: ")
scores = []
for i in range(1, 6):
    score= float(input(f"enter score {i}:"))
    scores.append(score)


average_score= sum(scores)/len(scores)
highest_score = max(scores)
lowest_score = min(scores)

distinction_count = 0
fail_count = 0

for score in scores:
    if score >= 70:
        distinction_count += 1
    if score < 45:
        fail_count += 1


if average_score >= 70:
    final_grade = "Distinction"
elif average_score >= 60:
    final_grade = "Merit"
elif average_score >= 50:
    final_grade = "Pass"
else:
    final_grade = "Fail"    

# student scores report

print(f"Name: {name}")
print(f"Scores: {scores}")
print(f"Average Score: {average_score:.2f}")
print(f"Highest Score: {highest_score:.2f}")
print(f"Lowest Score: {lowest_score:.2f}")
print(f"Number of Distinctions: {distinction_count}")
print(f"Number of Fails: {fail_count}")
print(f"Final Grade: {final_grade}")