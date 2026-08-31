from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()

tasks = [
    {
        "id": 1,
        "title": "Learn Python",
        "completed": True
    },
    {
        "id": 2,
        "title": "Learn FastAPI",
        "completed": False
    },
    {
        "id": 3,
        "title": "Build Task API",
        "completed": False
    }
]


class Task_create(BaseModel):
    title: str
    completed: bool= False

@app.post('/tasks',status_code=201)
def create_task(new_task: Task_create):

    if not tasks:
        new_id = 1
    else:
        new_id = max(item['id'] for item in tasks) + 1


    task_dict= new_task.model_dump()

    task_dict['id']= new_id

    tasks.append(task_dict)

    return task_dict

@app.get('/tasks')
def get_tasks():
    return tasks


class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None
    
@app.patch("/tasks/{task_id}")
def update_task(task_id: int, data: TaskUpdate):

    for item in tasks:

        if item["id"] == task_id:

            update_data = data.model_dump(exclude_unset=True)

            item.update(update_data)

            return item

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )

    
# Why does GET /tasks now show the newly created task?
#
# Answer:cause the post task has created a new data and appended it on tasks

# What value did completed receive?
#
# Answer:false

# Why?
#
# Answer:cause false is the default value

# Did my create_task function successfully create the task?
#
# Answer:no

# Why was the request rejected?
#
# Answer:cause the mandatory value was missing


# Question 1:
# What is a request body?
#
# Answer:is a body that defines the data we are sending


# Question 2:
# What is BaseModel being used for today?
#
# Answer:it is used for providing constraints to a given data


# Question 3:
# In TaskCreate, why doesn't the client need to
# provide an id?
#
# Answer:cause it will cause data conflict if not uniquely given


# Question 4:
# What does completed: bool = False mean?
#
# Answer:default value is false


# Question 5:
# What does model_dump() give us?
#
# Answer:gives us a python data structures


# Question 6:
# What does tasks.append(...) do?
#
# Answer:it stores data a the end of an array


# Question 7:
# Why is len(tasks) + 1 not always safe for IDs?
#
# Answer:cause if a data before it is deleted it won't be organized 


# Question 8:
# What is the main difference between POST and PATCH?
#
# Answer:create and update


# Question 9:
# Why should fields in TaskUpdate be optional?
#
# Answer: cause you don't need to update all data 


# Question 10:
# What should happen if PATCH /tasks/500 is requested
# but task 500 does not exist?
#
# Answer: 404