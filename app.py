from fastapi import FastAPI, Depends
from routers.product import product_router
from routers.user import user_router
from routers.auth import auth_router
from routers.admin import admin_router
from routers.order import order_router
import mysql.connector
import os
from dotenv import load_dotenv
from create_admin import create_admin
from ecommercedb import Users

app = FastAPI()
app.include_router(product_router)
app.include_router(admin_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(order_router)
load_dotenv()

@app.on_event("startup")
def start_up():
    app.state.db = mysql.connector.connect(
            host=os.getenv('dbhost'),
            user=os.getenv('dbuser'),
            password=os.getenv('dbpassword'),
            database=os.getenv('dbname')
        )
    create_admin(app.state.db)

"""
USERS/ADMIN
#create default admin on start
normal - #view products
         #add to cart
         #view order
         #update order
         #delete order
         #checkout
	     #register
	     #login
	     #change password admin login
	    
admin - #view products
        #update product list
        #delete product
        #view users
	    #create admin user
	    #delete user
	    #update password of user 

DATABASE
users > orders > order_items > products

BACKEND (ROUTES)
order
/create_order
/view_order
/update
/delete
/for_checkout
/checkout

products
/list_product
/product_delete - admin
/product_update - admin

user
/register
/password_update - admin
/delete_user - admin

admin
/admin_registration
/view_users
/user_disable
/user_activate
/delete_user
/product_update
/product_delete

AUTHENTICATION
#generate token
#protect routes

HTML (BASIC DISPLAY) 
"""