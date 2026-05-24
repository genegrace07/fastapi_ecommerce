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



