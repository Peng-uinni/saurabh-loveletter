from passlib.context import CryptContext

from . import config

pwd_context = CryptContext(schemes=['bcrypt'])

def verify_password(plain_pwd:str, hashed_pwd:str):
    try:
        return pwd_context.verify(plain_pwd, hashed_pwd)
    except:
        return plain_pwd == hash_pwd

def hash_pwd(plain_pwd:str):
    return pwd_context.hash(plain_pwd)