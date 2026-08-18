import json

student ={
    "name": "mamba",
    "student_id": "22CD032176",
    "score": [78,76,97],
    "active": True
}

print(student)
print(type(student))

student_json= json.dumps(student,indent= 4)
print(student_json)
print(type(student_json))

student_python = json.loads(student_json)
print(student_python)
print(type(student_python))