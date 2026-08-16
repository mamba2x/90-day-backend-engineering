class Student:
    def __init__(self, name, scores, student_id):
        self.name = name
        self.scores = scores
        self.student_id = student_id

    def calculate_average(self):
        return sum(self.scores) / len(self.scores)

    def find_highest(self):
        return max(self.scores)

    def find_lowest(self):
        return min(self.scores)

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