#Importing the FastApi class
from fastapi import FastAPI, Response, status
from fastapi.responses import JSONResponse

description = """
MyApp API helps you to manage your works which are to be done.

## Works

You can see your **Todos**.

## Locations

You can manage works:

* **At Home** .
* **At Office** .
"""


# Creating an app object
homeapp = FastAPI( title="MyApp",
    description=description,
    version="0.0.1",
    terms_of_service="http://myapp.com/terms/",
    contact={
        "name": "Zain Amjad Basra",
        "email": "zainamjadbasra@gmail.com",
    },)
officeapp = FastAPI( title="MyApp",
    description=description,
    version="0.0.1",
    terms_of_service="http://myapp.com/terms/",
    contact={
        "name": "Zain Amjad Basra",
        "email": "zainamjadbasra@gmail.com",
    },)


# A minimal app to demonstrate the get request 
@homeapp.get("/", tags=['root'])
async def root() -> dict:
    return {"Ping": "Pong"}

@officeapp.get("/", tags=['root'])
async def root() -> dict:
    return {"Ping": "Pong"}


# GET -- > Read Todo 
@homeapp.get("/todo", tags=['Home Todos'])
async def get_todos(response: Response):
    response.headers["hello"] = "here are your todos."
    return {"Data": hometodos}

@officeapp.get("/todo", tags=['Todos'])
async def get_todos(response: Response):
    response.headers["hello"] = "here are your todos."
    return {"Data": officetodos}

# Post -- > Create Todo
@homeapp.post("/todo", tags=["Home Todos"])
async def add_todo(todo: dict) -> dict:
    hometodos.append(todo)
    return JSONResponse(status_code=201, content={"data": "A Todo is Added in Todos!"})

@officeapp.post("/todo", tags=["Todos"])
async def add_todo(todo: dict) -> dict:
    officetodos.append(todo)
    return JSONResponse(status_code=201, content={"data": "A Todo is Added in Todos!"})

# PUT  -- > Update Todo
@homeapp.put("/todo/{id}",status_code=200, tags=["Home Todos"])
async def update_todo(id: int, body: dict, response: Response) -> dict:
    for todo in hometodos:
        if (int(todo["id"])) == id:
            todo["Activity"] = body["Activity"]
            return {
                "data": f"Todo with id {id} has been updated"
            }
        else:
            response.status_code = status.HTTP_201_CREATED
            return {"data": f"The Todo with id {id} is not found!"}

@officeapp.put("/todo/{id}",status_code=200, tags=["Todos"])
async def update_todo(id: int, body: dict, response: Response) -> dict:
    for todo in officetodos:
        if (int(todo["id"])) == id:
            todo["Activity"] = body["Activity"]
            return {
                "data": f"Todo with id {id} has been updated"
            }
        else:
            response.status_code = status.HTTP_201_CREATED
            return {"data": f"The Todo with id {id} is not found!"}

# DELETE --> Delete Todo 
@homeapp.delete("/todo/{id}", tags=["Home Todos"])
async def delete_todo(id: int) -> dict:
    for todo in hometodos:
        if int(todo["id"]) == id:
            hometodos.remove(todo)
            return{
                "data": f"Todo with id {id} has been deleted!"
            }
    return {
        "data": f"Todo with id {id} was not found!"
    }

@officeapp.delete("/todo/{id}", tags=["Todos"])
async def delete_todo(id: int) -> dict:
    for todo in officetodos:
        if int(todo["id"]) == id:
            officetodos.remove(todo)
            return{
                "data": f"Todo with id {id} has been deleted!"
            }
    return {
        "data": f"Todo with id {id} was not found!"
    }

# Home Todos List

hometodos = [
    {
        "id": "1",
        "Activity": "Jogging for 2 hours at 7:00 AM."
    },
    {
        "id": "2",
        "Activity": "Writing 3 pages of my new book at 2:00 PM."
    }
]

#Office Todos List

officetodos = [
    {
        "id":"1",
        "Activity": "Read the docomantation."
    },
    {
        "id":"2",
        "Activity": "Code the logic."
    }
]


homeapp.mount("/subapi", officeapp)