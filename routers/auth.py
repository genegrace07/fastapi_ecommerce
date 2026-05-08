from fastapi import APIRouter,Depends,Request,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from passlib.hash import sha256_crypt
from jose import jwt
from datetime import timedelta,datetime
import os
from dotenv import load_dotenv
from verify import verify_token
from ecommercedb import Users

auth_router = APIRouter(prefix='/auth',tags=['auth'])
ALGORITHM = 'HS256'
token_exp = 20
SECRET_KEY = os.getenv('SECRET_KEY')

def user_service(request:Request):
    return Users(request.app.state.db)

@auth_router.post('/user_login')
async def users_login(form:OAuth2PasswordRequestForm=Depends(),service:Users=Depends(user_service)):
    username = form.username
    password = form.password
    check_username = service.get_username(username)
    if not check_username:
        raise HTTPException(status_code=400,detail='username not found')
    check_password = sha256_crypt.verify(password,check_username['passwd'])
    if not check_password:
        raise HTTPException(status_code=400,detail='wrong password')
    payload = {"id":check_username['user_id'],"username":check_username['username'],"exp":datetime.utcnow()+timedelta(minutes=token_exp)}
    for_token = jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return {'token':for_token,"token_type":"bearer"}






