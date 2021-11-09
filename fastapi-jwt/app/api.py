from fastapi import FastAPI, Body, Depends

from .model import User, NewPasswordCredentials

import re

from .auth.auth_bearer import JWTBearer
from .auth.auth_handler import sign_token

app = FastAPI()

trial_users = [
    {
        "id": 1,
        "username": "amirhossein",
        "password": "pass1584"
    },
    {
        "id": 2,
        "username": "alireza",
        "password": "pass4589"
    },
]


@app.get("/", tags=["root"])
def read_root() -> dict:
    return {"message": "welcome to jwt app"}


@app.post("/api/auth/api_key", tags=["jwt"])
def get_jwt(user_credentials: User = Body(..., embed=True)):
    for user in trial_users:
        if user_credentials.username == user["username"]:
            token = sign_token(user_credentials.username)
            return {"token": token}
        else:
            continue
    return {"message": "the user was not found"}


@app.get("/api/auth/me/", dependencies=[Depends(JWTBearer())], tags=["details"])
def get_user_by_id(user_id: int):
    for user in trial_users:
        if user.get("id") == user_id:
            return user
        else:
            continue
    return {
        "message": "the user was not found or incorrect id submitted"
    }


@app.put("/api/users/reset_password/", dependencies=[Depends(JWTBearer())], tags=["reset_pass"])
def reset_pasword(credentials: NewPasswordCredentials = Body(..., embed=True)):
    for user in trial_users:
        if user.get("username") == credentials.username:
            if len(credentials.new_password) <= 8 and bool(re.match("^[a-zA-Z0-9_]+$", credentials.new_password)):
                user["password"] = credentials.new_password
                return {
                    "message": "your password has been changed successfully"
                }
            else:
                return {
                    "message": "your password is incorrect"
                }
        else:
            continue
    return {
        "message": "the user was not found or incorrect password"
    }
