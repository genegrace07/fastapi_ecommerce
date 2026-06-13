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

    get_product = product_services.get_product(id)
    item_name = get_product.get('item')
    user_id = payload.get('id')
    customer_name = payload.get('username')
    total = quantity * get_product.get('price')
    price = get_product.get('price')
    has_pending = order_services.has_pending(user_id)
    # status = has_pending.get('status')
    # print(has_pending)
    if has_pending:
        order_id = has_pending['order_id']
        order_services.add_to_order_item(id,order_id,quantity,item_name,price,total)
        grand_total = order_services.get_grand_total(order_id)
        order_services.update_grand_total(order_id, grand_total)
        order_count = order_services.get_order_count(order_id)
        order_services.update_order_count(user_id,order_count)
        # print(order_count)
        return {'message':'cart update successfully'}
    order_services.create_order(user_id,customer_name)
    get_order_id = order_services.create_new_order(user_id)
    order_id = get_order_id.get('order_id')
    order_services.add_to_order_item(id,order_id,quantity,item_name,price,total)
    grand_total = order_services.get_grand_total(order_id)
    order_services.update_grand_total(order_id, grand_total)
    order_count = order_services.get_order_count(order_id)
    order_services.update_order_count(user_id, order_count)
    print(order_count)
    return {'message':'item added successfully'}
@order_router.get('/order_view')
def view_order(payload:dict=Depends(verify_token),order_services:Order=Depends(order_service)):
    user_id = payload.get('id')
    order_id = order_services.create_new_order(user_id)
    order_id = order_id['order_id']
    orders = order_services.view_order(order_id)
    print(orders)
    print(order_id)
    return orders


#ALWAYS UPDATE GIT
#NOTE: jinbei is admin, brook is user only
#ONGOING: view order, done adding view order route, next is organize json output
#create user delete permanent with on cascade

'''
TO BE CONTINUE:  always update git
                 normal user - 
                 #view products
                 #add to cart
                 view order
                 update order
                 delete order
                 checkout
                 #register
                 #login
                 change password admin login

[
  {
    "user_id": 1,
    "username": "admin",
    "role": "admin"
  },
  {
    "user_id": 3,
    "username": "brook",
    "role": "user"
  },
  {
    "user_id": 19,
    "username": "jinbei",
    "role": "admin"
  },
  {
    "user_id": 20,
    "username": "sanji",
    "role": "user"
  },
  {
    "user_id": 21,
    "username": "chopper",
    "role": "user"
  },
  {
    "user_id": 22,
    "username": "franky",
    "role": "admin"
  },
  {
    "user_id": 23,
    "username": "luffy",
    "role": "user"
  }
]
'''