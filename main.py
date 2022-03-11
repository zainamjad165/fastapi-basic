from fastapi import FastAPI, Response, status
from fastapi.responses import JSONResponse
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

description = """
TODOApp API helps you to manage your works which are to be done.

## Works

You can see your **Todos**.

## Locations

You can manage works:

* **At Home** .
* **At Office** .
"""

fake_users_db = {
    "zain": {
        "username": "zain",
        "full_name": "zain amjad",
        "email": "zain@gamil.com",
        "hashed_password": "fakehashedzain",
        "disabled": False,
    },
    "sami": {
        "username": "sami",
        "full_name": "sami basra",
        "email": "sami@gmail.com",
        "hashed_password": "fakehashedsami",
        "disabled": False,
    },
}

def fake_hash_password(password: str):
    return "fakehashed" + password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user



homeapp = FastAPI( title="TODO App",
    description=description,
    version="0.0.1",
    terms_of_service="http://myapp.com/terms/",
    contact={
        "name": "Zain Amjad Basra",
        "email": "zainamjadbasra@gmail.com",
    },)

@homeapp.get("/", tags=['root'])
async def root() -> dict:
    return {"Ping": "Pong"}

@homeapp.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user.username, "token_type": "bearer"}

@homeapp.get("/seetodos", tags=['Home Todos'])
async def get_todos(response: Response,current_user: User = Depends(get_current_active_user)):
    response.headers["hello"] = "here are your todos."
    return {"Data": hometodos}


@homeapp.post("/addtodo", tags=["Home Todos"])
async def add_todo(todo: dict,current_user: User = Depends(get_current_active_user)) -> dict:
    officetodos.append(todo)
    return JSONResponse(status_code=201, content={"data": "A Todo is Added!"})

@homeapp.put("/updatetodo/{id}",status_code=200, tags=["Home Todos"])
async def update_todo(id: int, body: dict, response: Response,current_user: User = Depends(get_current_active_user)) -> dict:
    for todo in hometodos:
        if (int(todo["id"])) == id:
            todo["Activity"] = body["Activity"]
            return {
                "data": f"Todo with id {id} has been updated"
            }
        else:
            return {"data": f"The Todo with id {id} is not found!"}

@homeapp.delete("/deletetodo/{id}", tags=["Home Todos"])
async def delete_todo(id: int,current_user: User = Depends(get_current_active_user)) -> dict:
    for todo in hometodos:
        if int(todo["id"]) == id:
            hometodos.remove(todo)
            return{
                "data": f"Todo with id {id} has been deleted!"
            }
    return {
        "data": f"Todo with id {id} was not found!"
    }

hometodos = [
    {
        "id": "1",
        "Activity": "Jogging for 2 hours at 7:00 AM." 
    },
    {
        "id": "2",
        "Activity": "reading 3 pages of my new book at 2:00 PM."
    }
]


officeapp = FastAPI( title="TODO App",
    description=description,
    version="0.0.1",
    terms_of_service="http://myapp.com/terms/",
    contact={
        "name": "Zain Amjad Basra",
        "email": "zainamjadbasra@gmail.com",
    })

@officeapp.get("/", tags=['root'])
async def root() -> dict:
    return {"Ping": "Pong"}

@officeapp.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user.username, "token_type": "bearer"}


@officeapp.get("/seetodos", tags=['Office Todos'])
async def get_todos(response: Response,current_user: User = Depends(get_current_active_user)):
    response.headers["hello"] = "here are your todos."
    return {"Data": officetodos}

@officeapp.post("/addtodo", tags=["Office Todos"])
async def add_todo(todo: dict,current_user: User = Depends(get_current_active_user)) -> dict:
    officetodos.append(todo)
    return JSONResponse(status_code=201, content={"data": "A Todo is Added!"})

@officeapp.put("/updatetodo/{id}",status_code=200, tags=["Office Todos"])
async def update_todo(id: int, body: dict, response: Response,current_user: User = Depends(get_current_active_user)) -> dict:
    for todo in officetodos:
        if (int(todo["id"])) == id:
            todo["Activity"] = body["Activity"]
            return {
                "data": f"Todo with id {id} has been updated"
            }
        else:
            return {"data": f"The Todo with id {id} is not found!"}

@officeapp.delete("/deletetodo/{id}", tags=["Office Todos"])
async def delete_todo(id: int,current_user: User = Depends(get_current_active_user)) -> dict:
    for todo in officetodos:
        if int(todo["id"]) == id:
            officetodos.remove(todo)
            return{
                "data": f"Todo with id {id} has been deleted!"
            }
    return {
        "data": f"Todo with id {id} was not found!"
    }

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