# class student:
#     def __init__(self, name, score):
#         self.name=name
#         self.score = score

#     def student_grade(self):
#         if self.score>=70:
#             return "A"
#         elif self.score>=60:
#             return "B"
#         elif self.score>=50:
#             return "C"

# student1 = student("Emeka", 58)
# student2 = student("nonso", 78)

# print(f"the student score is: {student1.student_grade()}")
# print(student2.name)

# Account balance

class BankAccount:
    def __init__(self,balance,owner):
        self.balance=balance
        self.owner=owner

    def deposit(self,amount):
        self.balance+=amount

    def withdraw(self, amount):
        if amount >= self.balance:
            print("insufficient funds")
        else:
            self.balance-=amount
            return "Withdraw successful"
    def get_Balance(self):
        return self.balance
