# fastapi django flask
# fastapi

from fastapi import FastAPI

app = FastAPI()


# login
# path, method -> 
# http://127.0.0.1:8000/auth/login

@app.post("/auth/login")
def login():
    print("login success")

    return { "result": "sucess", "message": "login success", "data": { "user_id": 1, "token": "asgasgasgasgasg" } }


@app.get("/get-user-data")
def get_data():

    return { "user_id": 1, "token": "asgasgasgasgasg" }

