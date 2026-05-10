from fastapi import APIRouter,Request,Depends,HTTPException
from ecommercedb import Product
from verify import verify_token

product_router = APIRouter(prefix='/product',tags=['product'])

def product_service(request:Request):
    return Product(request.app.state.db)
@product_router.get('/product_lists')
def list_product(service:Product=Depends(product_service),check_token:dict=Depends(verify_token)):
    if not check_token:
        raise HTTPException(status_code=401,detail='token expired or invalid')
    return service.product_list()

