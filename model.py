from pydantic import BaseModel

class User(BaseModel):
    username:str="username"
    password:str="password"
