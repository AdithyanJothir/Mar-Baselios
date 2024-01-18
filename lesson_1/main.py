from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse


app = FastAPI()


class User(BaseModel):
    name: str
    age: int
    hometown: str


users: list[User] = []


@app.get("/")
def read_root():
    return {"Hello": "There"}


@app.post("/users", status_code=201)
def create_user(user: User):
    users.append(user)
    return users


@app.get("/users")
def list_users():
    user_models = [User.model_validate(each) for each in users]
    return user_models


@app.get("/users/{name}", response_model=User)
def get_user(name: str):
    for each in users:
        if each.name == name:
            return each
    return JSONResponse({"message": "user not found"}, status_code=404)


@app.put("/users/{name}")
def update_user(name: str, user: User):
    for each in users:
        if each.name == name:
            users.pop(users.index(each))
            users.append(user)
            return user
    return JSONResponse({"message": "user not found"}, status_code=404)


@app.delete("/users/{name}")
def delete_user(name: str):
    for user in users:
        if user.name == name:
            users.pop(users.index(user))
    return users
