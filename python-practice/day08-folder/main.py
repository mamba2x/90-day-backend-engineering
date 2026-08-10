import calculator

scores=[]

for i in range(1,6):
    score= calculator.get_valid_scores(i)
    scores.append(score)

average = calculator.calculate_average(scores)
highest = calculator.calculate_highest(scores)
lowest = calculator.calculate_lowest(scores)
grade = calculator.calculate_grade(average)
distinction_count = calculator.number_of_passes(scores)
fail_count = calculator.number_of_fails(scores)

print ("student scores details are:")
print(f"the highest score is:{highest}")
print(f"the lowest score is:{lowest}")
print(f"the grade score is:{grade}")
print(f"the distinction score is:{distinction_count}")
print(f"the fail count is:{fail_count}")
print(f"the average score is:{average}")
