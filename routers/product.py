from fastapi import APIRouter,Request,Depends
from ecommercedb import Product
from verify import verify_token

product_router = APIRouter(prefix='/product',tags=['product'])

def product_service(request:Request):
    return Product(request.app.state.db)
@product_router.get('/product_lists')
def list_product(service:Product=Depends(product_service),_:dict=Depends(verify_token)):
        return service.product_list()



