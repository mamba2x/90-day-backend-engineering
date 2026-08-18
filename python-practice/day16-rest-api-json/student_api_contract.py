def describe_endpoint(method, path):

    if method == "GET" and path.startswith("/students/"):
        student_id = path.split("/")[2]
        return f"Retrieve student: {student_id}"

    elif method == "PATCH" and path.startswith("/students/"):
        student_id = path.split("/")[2]
        return f"Update student: {student_id}"

    elif method == "DELETE" and path.startswith("/students/"):
        student_id = path.split("/")[2]
        return f"Delete student: {student_id}"

    elif method == "GET" and path == "/students":
        return "Retrieve all students"

    elif method == "POST" and path == "/students":
        return "Create new student"

    else:
        return "Endpoint not Found"    

print(describe_endpoint("GET", "/students/22cd032179"))
print(describe_endpoint("PATCH", "/students/22cd032179"))
print(describe_endpoint("DELETE", "/students/22cd032179"))
print(describe_endpoint("GET", "/students"))
print(describe_endpoint("POST", "/students"))
print(describe_endpoint("PUT", "/students"))
