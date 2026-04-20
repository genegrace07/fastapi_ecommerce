from fastapi import APIRouter
from ecommercedb import Product

class_product = Product()

product_router = APIRouter(prefix='/product',tags=['product'])

@product_router.get('/product_lists')
def list_product():
    return class_product.product_list()
