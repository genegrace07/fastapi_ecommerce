import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

class Dbconnection():
    def __init__(self,db):
        self.db = db

class Product(Dbconnection):
    def product_list(self):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'select * from product'
        dbcursor.execute(query)
        result = dbcursor.fetchall()
        dbcursor.close()
        return result
    def update_product(self,product_id,item,price,quantity):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'update product set item=%s,price=%s,quantity=%s where product_id=%s'
        dbcursor.execute(query,(item,price,quantity,product_id))
        dbcursor.close()
        self.db.commit()
    def get_product(self,product_id):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'select * from product where product_id = %s'
        dbcursor.execute(query,(product_id,))
        result = dbcursor.fetchone()
        dbcursor.close()
        return result
    def delete_product(self,product_id):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'delete from product where product_id = %s'
        dbcursor.execute(query,(product_id,))
        dbcursor.close()
        self.db.commit()
class Users(Dbconnection):
    def get_users(self):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'select * from user'
        dbcursor.execute(query)
        result = dbcursor.fetchall()
        dbcursor.close()
        return result
    def save_user(self,username,pwd,role):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'insert into user(username,passwd,roles) values(%s,%s,%s)'
        dbcursor.execute(query,(username,pwd,role))
        dbcursor.close()
        self.db.commit()
    def get_username(self,username):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'select * from user where username = %s'
        dbcursor.execute(query,(username,))
        result = dbcursor.fetchone()
        dbcursor.close()
        return result
    def get_user_id(self,id):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'select * from user where user_id = %s'
        dbcursor.execute(query,(id,))
        result = dbcursor.fetchone()
        dbcursor.close()
        return result
    def update_password(self,id,password):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        querry = 'update user set passwd=%s where user_id=%s'
        dbcursor.execute(querry,(password,id,))
        dbcursor.close()
        self.db.commit()
    def delete_user(self,id):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'delete from user where user_id=%s'
        dbcursor.execute(query,(id,))
        dbcursor.close()
        self.db.commit()
    def disable_user(self,id):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'update user set active = false where user_id = %s'
        dbcursor.execute(query,(id,))
        dbcursor.close()
        self.db.commit()
    def activate_user(self, id):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True, buffered=True)
        query = 'update user set active = true where user_id = %s'
        dbcursor.execute(query, (id,))
        dbcursor.close()
        self.db.commit()
    def get_active_user(self, id):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True, buffered=True)
        query = 'select * from user where user_id = %s and active = true'
        dbcursor.execute(query, (id,))
        result = dbcursor.fetchone()
        dbcursor.close()
        return result

class Order(Dbconnection):
    def create_order(self,user_id,customer_name):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'insert into orders(user_id,customer_name) values(%s,%s)'
        dbcursor.execute(query,(user_id,customer_name))
        self.db.commit()
        order_id = dbcursor.lastrowid
        dbcursor.close()
        return order_id
    def add_to_order_item(self,product_id,order_id,quantity,item_name,price,total):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'insert into order_item(product_id,order_id,quantity,item_name,price,total) values(%s,%s,%s,%s,%s,%s)'
        dbcursor.execute(query,(product_id,order_id,quantity,item_name,price,total))
        dbcursor.close()
        self.db.commit()
    def store_order(self,product_id,order_id,quantity,item_name,total):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'insert into order_item(product_id,order_id,quantity,item_name,total) values(%s,%s,%s,%s,%s)'
        dbcursor.execute(query,(product_id,order_id,quantity,item_name,total))
        dbcursor.close()
        self.db.commit()
    def has_pending(self,user_id):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'select * from orders where user_id = %s and status = "pending"'
        dbcursor.execute(query,(user_id,))
        result = dbcursor.fetchone()
        dbcursor.close()
        return result
    def create_new_order(self,user_id):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'select * from orders where user_id = %s'
        dbcursor.execute(query,(user_id,))
        result = dbcursor.fetchone()
        dbcursor.close()
        return result
    def get_order(self,order_id):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'select * from orders where order_id = %s'
        dbcursor.execute(query,(order_id,))
        result = dbcursor.fetchone()
        dbcursor.close()
        return result
    def get_order_item(self,order_id):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'select * from order_item where order_id = %s'
        dbcursor.execute(query,(order_id,))
        result = dbcursor.fetchone()
        dbcursor.close()
        return result
    def get_order_id(self,order_id,status):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'select * from orders where order_id = %s and status = "pending"'
        dbcursor.execute(query,(order_id,status))
        result = dbcursor.fetchone()
        dbcursor.close()
        return result
    def get_grand_total(self,order_id):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'select sum(total) as grand_total from order_item where order_id = %s'
        dbcursor.execute(query,(order_id,))
        result = dbcursor.fetchone()
        dbcursor.close()
        return result['grand_total']
    def update_grand_total(self,order_id,grand_total):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'update orders set grand_total = %s where order_id = %s'
        dbcursor.execute(query,(grand_total,order_id))
        dbcursor.close()
        self.db.commit()
    def get_order_count(self,order_id):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'select count(item_name) as order_counts from order_item where order_id = %s'
        dbcursor.execute(query,(order_id,))
        result = dbcursor.fetchone()
        dbcursor.close()
        return result['order_counts']
    def update_order_count(self,user_id,order_count):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'update orders set order_count = %s where user_id = %s'
        dbcursor.execute(query,(order_count,user_id))
        dbcursor.close()
        self.db.commit()
    def view_order(self,order_id):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = '''select oi.id,oi.item_name,oi.quantity,oi.price,oi.total from orders as o 
                   join order_item as oi on o.order_id = oi.order_id
                   where o.order_id = %s
                '''
        dbcursor.execute(query,(order_id,))
        result = dbcursor.fetchall()
        dbcursor.close()
        return result
    def cancel_order(self,user_id):
        self.db.ping(reconnect=True)
        dbcursor = self.db.cursor(dictionary=True,buffered=True)
        query = 'update orders set status = "cancel" where user_id = %s'
        dbcursor.execute(query,(user_id,))
        dbcursor.close()
        self.db.commit()

