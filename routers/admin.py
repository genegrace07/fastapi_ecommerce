from fastapi import APIRouter,Depends,HTTPException,Request
from verify import verify_token
from ecommercedb import Users,Product
from passlib.hash import sha256_crypt
from model import User,Product as ProductModel

admin_router = APIRouter(prefix='/admin',tags=['admin'])
def user_service(request:Request):
    return Users(request.app.state.db)
def product_service(request:Request):
    return Product(request.app.state.db)
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
    view_users_no_pwd = [{'user_id':v.get('user_id'),'username':v.get('username'),'role':v.get('roles')} for v in view_users]
    return view_users_no_pwd
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
@admin_router.put('/update_product')
def product_update(form:ProductModel,service:Product=Depends(product_service),payload:dict=Depends(verify_token)):
    prod_id = form.product_id
    item = form.item
    price = form.price
    quantity = form.quantity
    if payload.get('roles') != 'admin':
        raise HTTPException(status_code=403,detail='no permission')
    data = service.product_list()
    get_product_id = [d['product_id'] for d in data]
    if prod_id not in get_product_id:
        raise HTTPException(status_code=404,detail='product id not found')
    specific_prod = service.get_product(prod_id)
    item =   specific_prod['item'] if item in [None,"","string"] else item
    price =  specific_prod['price'] if price <= 0 else price
    quantity =  specific_prod['quantity'] if quantity <= 0 else quantity
    service.update_product(prod_id,item,price,quantity)
    return {'message':'successfully updated'}
@admin_router.delete('/delete_product')
def product_delete(product_id:int,service:Product=Depends(product_service),payload:dict=Depends(verify_token)):
    if payload.get('roles') != 'admin':
        raise HTTPException(status_code=401,detail='no permission')
    data = service.product_list()
    product_id_list = [d['product_id'] for d in data]
    if product_id not in product_id_list:
        raise HTTPException(status_code=404,detail='product id not found')
    service.delete_product(product_id)
    return {'message':'deleted successfully'}
    
