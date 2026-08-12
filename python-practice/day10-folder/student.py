class Student:

    def __init__(self, name, scores, student_id):
        self.name = name
        self.scores = scores
        self.student_id = student_id

    def find_highest(self):
        return max(self.scores)

    def find_lowest(self):
        return min(self.scores)

    def calculate_average(self):
        return sum(self.scores) / len(self.scores)

    def calculate_grade(self):
        average = self.calculate_average()

        if average >= 70:
            return "Distinction"
        elif average >= 60:
            return "Merit"
        elif average >= 50:
            return "Pass"
        else:
            return "Fail"

    def display_report(self):
        print(f"Student: {self.name}")
        print(f"Student ID: {self.student_id}")
        print(f"Scores: {self.scores}")
        print(f"Average: {self.calculate_average():.2f}")
        print(f"Highest: {self.find_highest()}")
        print(f"Lowest: {self.find_lowest()}")
        print(f"Grade: {self.calculate_grade()}")