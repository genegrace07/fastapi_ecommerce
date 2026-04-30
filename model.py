from pydantic import BaseModel,constr

class User(BaseModel):
    username:str
    password:str
