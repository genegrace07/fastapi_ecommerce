from pydantic import BaseModel

class User(BaseModel):
    username:str="username"
    password:str="password"
class Product(BaseModel):
    product_id:int=0
    item:str|None=None
    price:int|None=None
    quantity:int|None=None