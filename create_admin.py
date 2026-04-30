from passlib.context import CryptContext
from passlib.hash import sha256_crypt
from ecommercedb import Users

pwd_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

def create_admin(db):
    user_service = Users(db)
    if_empty = user_service.get_users()
    if not if_empty:
        default_user = 'admin'
        password = '1234'
        hash_pwd = sha256_crypt.hash(password)
        role = 'admin'
        user_service.save_user(default_user,hash_pwd,role)