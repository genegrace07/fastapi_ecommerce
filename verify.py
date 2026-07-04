from fastapi import HTTPException,Depends,Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt,JWTError
import os
from dotenv import load_dotenv
from ecommercedb import Users

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = 'HS256'
bearer_scheme = OAuth2PasswordBearer(tokenUrl='/auth/user_login')

def user_service(request:Request):
    return Users(request.app.state.db)
def verify_token(token:str=Depends(bearer_scheme),user_service:Users=Depends(user_service)):
    try:
        verified = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id = verified.get('id')
        user_data = user_service.get_user_id(user_id)
        if not user_data:
            raise HTTPException(status_code=404,detail='account not found')
        get_active_status = user_data.get('active')
        if not get_active_status:
            raise HTTPException(status_code=403,detail='account inactive')
        return verified
    except JWTError:
        raise HTTPException(status_code=401,detail="invalid or token not found")

