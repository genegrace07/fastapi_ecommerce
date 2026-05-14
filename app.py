from fastapi import FastAPI, Depends
from routers.product import product_router
from routers.user import user_router
from routers.auth import auth_router
from routers.admin import admin_router
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
         add to cart
         update order
         delete order
         checkout
	     #register
	     #login
	     change password admin login
	    
admin - view products
        update product list
        delete product
        #view users
	    #create admin user
	    delete user
	    update password of user 

DATABASE
users > orders > order_items
users > products
products > order_items
orders > order_items

BACKEND (ROUTES)
order
/create_order
/update
/delete
/checkout
/view_order_summary

products
/view_products
/delete_products - admin
/update_products - admin

user
/register
/change_password
/delete_user - admin
/update_password_of_any_user - admin

AUTHENTICATION
generate token
protect routes

HTML (BASIC DISPLAY) 
"""