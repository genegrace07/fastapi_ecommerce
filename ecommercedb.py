import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

db = mysql.connector.connect(
    host=os.getenv('dbhost'),
    user=os.getenv('dbuser'),
    password=os.getenv('dbpassword'),
    database=os.getenv('dbname')
)

class Product():
    def product_list(self):
        db.ping(reconnect=True)
        dbcursor = db.cursor(dictionary=True,buffered=True)
        querry = 'select * from product'
        dbcursor.execute(querry)
        result = dbcursor.fetchall()
        dbcursor.close()
        return result



