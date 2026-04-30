from fastapi import APIRouter,Request,Depends,Form,HTTPException
from ecommercedb import Users
from model import User
from passlib.hash import sha256_crypt

user_router = APIRouter(prefix='/user',tags=['user'])
def user_service(request:Request):
    return Users(request.app.state.db)
@user_router.post('/register')
async def register_user(form:User,service:Users=Depends(user_service)):
    username = form.username
    password = form.password
    view_users = service.get_username(username)
    if not username or not str(username).strip() or not password or not str(password).strip():
        raise HTTPException(status_code=400,detail='username or password cannot be blank')
    if view_users:
        raise HTTPException(status_code=400,detail='username already exist')
    hash_pwd = sha256_crypt.hash(password)
    service.save_user(username,hash_pwd,role='user')
    return {'message':'added successfully'}
@user_router.post('/register_admin')
async def admin_registration(form:User,service:Users=Depends(user_service)):
    username = form.username
    password = form.password
    get_user = service.get_username(username)
    if not username or not str(username).strip() or not password or not str(password).strip():
        raise HTTPException(status_code=400, detail='username or password cannot be blank')
    if get_user:
        raise HTTPException(status_code=400,detail='username already exist')
    hash_pwd = sha256_crypt.hash(password)
    service.save_user(username,hash_pwd,role='admin')
    return {'message':'added successfully'}

#DUPLICATE USERNAME THRU MYSQL? ADMIN OR NORMAL USER FOR REGISTRATION?
#COMMIT AND PUSH TO GIT, (user registration)
