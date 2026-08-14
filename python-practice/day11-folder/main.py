from course import course
from student import student
from department import department

department1 = department("computer-science","CIS")
department2 = department("MIS","CIS")

course1 = course("Software Engineering", "CSC425",department1)
course2 = course("Human and Computer Interaction", "CSC441",department2)

student1 = student("mamba","22CD032179", [32,54,47,96], course1)
student2 = student("Micheal","22CD032139", [32,54,47,96], course1)
student3 = student("divine","22CD032177", [92,64,77,66], course2)



student1.report_student_scores()
student2.report_student_scores()
student3.report_student_scores()