from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

class UserToken(BaseModel):
    username:str

def create_access_token(data:dict):
    pass