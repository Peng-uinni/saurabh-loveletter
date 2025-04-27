from fastapi import APIRouter, Request, Form, HTTPException, Depends, status, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from pydantic import BaseModel
from typing import Annotated
from datetime import timedelta

from pages.templating import templates, context
from database.users import get_user_data, create_user, get_db, Users
from database.posts import get_user_posts
from auth.token import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user
from auth.token import create_access_token

from pages.templating import context

router = APIRouter(
    prefix="/users"
)

#data schemas
class UserLoginData(BaseModel):
    username:str
    password:str

class UserSignUpData(BaseModel):
    username:str
    name:str
    email:str
    password:str

#endpoints
@router.get("/login", response_class=HTMLResponse)
async def login_page(request:Request):
    con = context.null_context().model_dump()
    return templates.get_template(request=request, name="login.html", context=con)

@router.post("/login", response_class=RedirectResponse)
async def login_form(
    form_data:Annotated[UserLoginData, Form()],
    db:Annotated[Session, Depends(get_db)]):

    try:
        response.delete_cookie("access_token")
    except:
        pass

    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:  
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    token = create_access_token({"sub":form_data.username})

    response = RedirectResponse(url='/users/me', status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        key="access_token",
        value=token,
        expires=ACCESS_TOKEN_EXPIRE_MINUTES * 6000,
        path="/",
        httponly=True
    )
    
    return response

@router.get("/signup")
async def signup_page(request:Request):
    con = context.null_context().model_dump()
    return templates.get_template(request=request, name="signup.html", context=con)

@router.post("/signup", response_class=RedirectResponse)
async def signup_form(
    form_data:Annotated[UserSignUpData, Form()], 
    db:Annotated[Session, Depends(get_db)]
    ):

    user = get_user_data(db, form_data.username)
    if user is None:
        create_user(db, form_data.model_dump())
    else:
        raise HTTPException(status_code=400, detail="Username is already taken")
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/me")
async def user_me(
    request:Request,
    user:Annotated[Users, Depends(get_current_user)],
    db:Annotated[Session, Depends(get_db)]
    ):

    posts = get_user_posts(user.username, db)

    con = context.PageContext(
        title=f"{user.username}",
        link_field=[""],
        username=str(user.username),
        name = str(user.name),
        posts=posts,
        logged_in=True
    )
    
    return templates.get_template(request=request, name="user.html", context=con.model_dump())
