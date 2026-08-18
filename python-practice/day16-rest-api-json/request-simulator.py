import json

students = [
    {
        "name": "Nonso",
        "student_id": "22CD032179",
        "scores": [78, 76, 97]
    }
]


def simulate_request(method, path, body=None):

    if method == "POST" and path == "/students":

        students.append(body)

        response = {
            "status_code": 201,
            "body": {
                "message": "Student created successfully",
                "student": body
            }
        }

        return response

    elif method == "GET" and path == "/students":

        response = {
            "status_code": 200,
            "body": {
                "students": students
            }
        }

        return response

    else:

        return {
            "status_code": 404,
            "body": {
                "message": "Endpoint not found"
            }
        }


student_data = {
    "name": "Mamba",
    "student_id": "22CD032180",
    "scores": [78, 76, 97]
}


post_response = simulate_request(
    "POST",
    "/students",
    student_data
)

get_response = simulate_request(
    "GET",
    "/students"
)

not_found_response = simulate_request(
    "POST",
    "/teachers",
    student_data
)


print(json.dumps(post_response, indent=4))

print(json.dumps(get_response, indent=4))

print(json.dumps(not_found_response, indent=4))