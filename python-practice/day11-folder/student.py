class student:
    def __init__(self,name,student_id,scores,course):
        self.name=name
        self.student_id=student_id
        self.scores=scores
        self.course=course

    def calculate_average(self):
        return sum(self.scores)/len(self.scores)

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
        
    def find_highest(self):
        return max(self.scores)

    def find_lowest(self):
        return min(self.scores)

    def report_student_scores(self):
          print(f"student: {self.name}")
          print(f"Student id: {self.student_id}")
          print(f"course: {self.course.report_course()}")
          print(f"department: {self.course.department_details()}")
          print(f"scores: {self.scores}")
          print(f"average: {self.calculate_average():.2f}")
          print(f"the highest score is: {self.find_highest()}")
          print(f"the lowest score is: {self.find_lowest()}")
          print(f"the grade: {self.calculate_grade()}")