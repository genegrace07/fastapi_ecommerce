from fastapi import APIRouter,Depends,HTTPException,Request
from verify import verify_token
from ecommercedb import Users
from passlib.hash import sha256_crypt
from model import User

admin_router = APIRouter(prefix='/admin',tags=['admin'])
def user_service(request:Request):
    return Users(request.app.state.db)

@admin_router.post('/register_admin')
async def admin_registration(form:User,service:Users=Depends(user_service),check_token:dict=Depends(verify_token)):
    username = form.username
    password = form.password
    get_user = service.get_username(username)
    if check_token['roles'] != 'admin':
        raise HTTPException(status_code=403,detail='no permission')
    if username == "username" or password == "password":
        raise HTTPException(status_code=400,detail="default cant be use, input username and password")
    if not username or not str(username).strip() or not password or not str(password).strip():
        raise HTTPException(status_code=400, detail='username or password cannot be blank')
    if get_user:
        raise HTTPException(status_code=400,detail='username already exist')
    hash_pwd = sha256_crypt.hash(password)
    service.save_user(username,hash_pwd,role='admin')
    return {'message':'added successfully'}

@admin_router.get('/view_user')
async def view_users(service:Users=Depends(user_service),payload:dict=Depends(verify_token)):
    if payload.get('roles') != 'admin':
        raise HTTPException(status_code=403,detail='no permission')
    view_users = service.get_users()
    return view_users
@admin_router.put('/update_password')
async def password_update(id:int,new_pwd:str,service:Users=Depends(user_service),payload:dict=Depends(verify_token)):
    if payload.get('roles') != 'admin':
        raise HTTPException(status_code=403,detail='no permission')
    get_id = service.get_user_id(id)
    if not get_id:
        raise HTTPException(status_code=404,detail='user id not found')
    if not new_pwd or not new_pwd.strip():
        raise HTTPException(status_code=400,detail='password cannot be blank')
    hash_password = sha256_crypt.hash(new_pwd)
    service.update_password(id,hash_password)
    return {'message':'password successfully updated'}
@admin_router.delete('/delete_user')
async def user_delete(id:int,service:Users=Depends(user_service),payload:dict=Depends(verify_token)):
    if payload.get('roles') != 'admin':
        raise HTTPException(status_code=403,detail='no permission')
    get_id = service.get_user_id(id)
    if payload.get('id') == id:
        raise HTTPException(status_code=400,detail='currently login, cannot be delete')
    if not get_id:
        raise HTTPException(status_code=404,detail='user id not found')
    service.delete_user(id)
    return {'message':'successfully deleted'}

#TO BE CONTINUE: delete user for admin access only,cannot be delete while login in, and update git
                #dont show pwd in view user
