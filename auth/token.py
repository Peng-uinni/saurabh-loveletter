from fastapi import Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordBearer

import jwt
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from typing import Annotated, Union

from database.engine import get_db, Session
from database.users import Users, get_user_data

from .password import verify_password
from .config import KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    username:str|None = None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def authenticate_user(db:Annotated[Session, Depends(get_db)], username:str, password:str):
    user = get_user_data(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data:dict, expires_delta:Union[timedelta, None] = None):
    #data contains the sub
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
        access_token: Annotated[str, Cookie()],
        db:Annotated[Session, Depends(get_db)]):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(access_token, KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    
    user = get_user_data(db, username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[Users, Depends(get_current_user)],
):
    return current_user