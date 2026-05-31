from fastapi import HTTPException,Request,APIRouter,Depends
from verify import verify_token
from ecommercedb import Order,Product

order_router = APIRouter(prefix='/order',tags=['order'])

def order_service(request:Request):
    return Order(request.app.state.db)
def product_service(request:Request):
    return Product(request.app.state.db)
@order_router.put('/add_order')
def create_order(id:int,quantity:int,payload:dict=Depends(verify_token),order_services:Order=Depends(order_service),product_services:Product=Depends(product_service)):
    product_list = product_services.product_list()
    get_product_id = [p['product_id'] for p in product_list]
    if id not in get_product_id:
        raise HTTPException(status_code=404,detail='product id not found')
    if quantity <= 0:
        raise HTTPException(status_code=400,detail='quantity must be greater than 0')

    user_id = payload.get('id')
    order_id = order_services.create_order(user_id)

    get_product = product_services.get_product(id)
    total = quantity * get_product.get('price')
    price = get_product.get('price')
    item_name = get_product.get('item')
    order_services.add_to_order_item(id,order_id,quantity,item_name,price,total)
    print(get_product)
    return {'message':'item added successfully'}

#ADD TO CART DONE, CREATE ANOTHER ROUTE FOR CHECKOUT
#NOTE: jinbei is admin, brook is user only
'''
    def store_order(self,product_id,order_id,quantity,item_name,total):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'insert into order_item(product_id,order_id,quantity,item_name,total) values(%s,%s,%s,%s,%s)'
        dbcursor.execute(query,(product_id,order_id,quantity,item_name,total))
        dbcursor.close()
        self.db.commit()
'''
'''
TO BE CONTINUE:  always update git
                 normal user - 
                 #view products
                 add to cart
                 update order
                 delete order
                 checkout
                 #register
                 #login
                 change password admin login

'''