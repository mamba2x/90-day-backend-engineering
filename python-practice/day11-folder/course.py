class course:
    def __init__(self, name, code, department):
        self.name =name
        self.code=code
        self.department=department

    def report_course(self):
        return f"{self.code} - {self.name}"
    
    def department_details(self):
        return f"{self.name} - {self.code} "
        

