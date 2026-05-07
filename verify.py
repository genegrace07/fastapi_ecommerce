from fastapi import HTTPException
from jose import jwt,JWTError
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = 'HS256'

def verify_token(token):
    try:
        verified = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return verified
    except JWTError:
        raise HTTPException(status_code=401,detail="invalid or token not found")