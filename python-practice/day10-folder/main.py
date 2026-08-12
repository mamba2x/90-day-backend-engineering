from bank_account import BankAccount
from student import Student
student1 = BankAccount(1500,"david")


# print(student1.get_Balance())
# print(student1.owner)
# student1.deposit(2000)
# print(student1.get_Balance())
# student1.withdraw(4500)
# print(student1.get_Balance())



student1 = Student(
    "Nonso",
    [78, 32, 68],
    "22CD032179"
)
student2 = Student(
    "Emeka",
    [78, 32, 68],
    "22CD032179"
)
student3 = Student(
    "Odin",
    [78, 32, 68],
    "22CD032179"
)

student1.display_report()
student2.display_report()
student3.display_report()


