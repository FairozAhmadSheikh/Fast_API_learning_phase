from pydantic import BaseModel


class UserSchema(BaseModel):
    name:str
    username:str
    email:str
    phone_number:int
    password:str

class LoginSchema(BaseModel):
    username:str
    password:str

class UserResponseSchema(BaseModel):
    user_id:int
    name:str
    username:str
    