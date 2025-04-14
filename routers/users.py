from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from pydantic import BaseModel
from typing import Annotated

from pages.templating import templates
from database.users import get_user_data, create_user, get_db, Users
from auth.token import oauth2_scheme

router = APIRouter(
    prefix="/users"
)

#data schemas
class UserLoginData(BaseModel):
    username:str
    password:str

class UserSignUpData(BaseModel):
    username:str
    email:str
    password:str

#user auth stuff
def get_current_user(token:Annotated[str, Depends(oauth2_scheme)], db:Annotated[Session, Depends(get_db)]):
    user = get_user_data(token, db)
    if user is None:
        return {"Aaaaa":"aaaa"}
    return user

#endpoints
@router.get("/login", response_class=HTMLResponse)
async def login_page(request:Request):
    return templates.get_template(request=request, name="login.html")

@router.post("/login")
async def login_form(user_data:Annotated[OAuth2PasswordRequestForm, Depends()], db:Annotated[Session, Depends(get_db)]):
    user = get_user_data(user_data.username, db)
    if user is None:
        raise HTTPException(status_code=400, detail="User doesn't exist")
    if user.password != user_data.password:
        raise HTTPException(status_code=400, detail="Incorrect Password")
    #generate token 
    return {"access_token": user_data.username, "token_type": "bearer"}   

@router.get("/signup")
async def signup_page(request:Request):
    return templates.get_template(request=request, name="signup.html")

@router.post("/signup")
async def signup_form(user_data:Annotated[UserSignUpData, Form()], db:Annotated[Session, Depends(get_db)]):
    user = get_user_data(user_data.username, db)
    if user is None:
        raise HTTPException(status_code=400, detail="Username is already taken")
    create_user(user_data.model_dump(), db)
    return 

@router.get("/me")
async def user_me(user:Annotated[Users, Depends(get_current_user)]):
    return user.model_dump()
