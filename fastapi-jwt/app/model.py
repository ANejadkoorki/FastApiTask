from pydantic import BaseModel, Field


class User(BaseModel):
    username: str = Field(..., min_length=4, max_length=30)
    password: str = Field(..., max_length=8, regex="^[a-zA-Z0-9_]+$")

    class Config:
        scheme_extra = {
            "example": {
                "username": "proper_username",
                "password": "pass123"
            }
        }


class NewPasswordCredentials(BaseModel):
    username: str = Field(..., min_length=4, max_length=30)
    new_password: str = Field(..., max_length=8, regex="^[a-zA-Z0-9_]+$")

    class Config:
        scheme_extra = {
            "example": {
                "username": "proper_username",
                "new_password": "pass123"
            }
        }
