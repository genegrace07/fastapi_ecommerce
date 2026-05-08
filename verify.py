from fastapi import HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt,JWTError
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = 'HS256'
bearer_scheme = OAuth2PasswordBearer(tokenUrl='/auth/user_login')

def verify_token(token:str=Depends(bearer_scheme)):
    try:
        verified = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return verified
    except JWTError:
        raise HTTPException(status_code=401,detail="invalid or token not found")