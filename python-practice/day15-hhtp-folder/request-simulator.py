def explain_method(method):
    if method == "GET":
        return "GET means the client wants to retrieve data."
    elif method == "POST":
        return "POST means the client wants TO CREATE SOMETHING."
    elif method == "PUT":
        return "PUT means the client wants to replace data."
    elif method == "PATCH":
        return "PATCH means the client wants to update data."
    elif method == "DELETE":
        return "DELETE means the client wants to remove data."

def classify_status_code(status_code):
    if status_code >=200 and status_code< 300:
        return "SUCCESS"
    elif status_code >=400 and status_code<500:
        return "CLIENT ERROR"
    elif status_code >=500 and status_code<600:
        return "SERVER ERROR"
    elif 300 <= status_code < 400:
        return "REDIRECTION"
    else:
        return "Unknown STATUS CODE"
while True:
    try:
        code= int(input("enter status code:"))
        path= input("enter path:")
        methods = input("Enter HTTP method:").strip().upper() 
        break
    except ValueError:
        print("enter a value:")
print("Request")
print("----------------------------")
print(f"Method: {methods}")
print(f"Path: {path}")
print("\n")
print(f"{explain_method(methods)}")
print("\n")
print("Response")
print("---------------------------")
print(f"Status code: {code}")
print(f"Category: {classify_status_code(code)}")


