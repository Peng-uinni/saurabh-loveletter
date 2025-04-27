from fastapi import Depends
from sqlmodel import SQLModel, Session, Field, select, func, desc, join
from typing import Annotated, Optional
from datetime import datetime
from pydantic import BaseModel

from .engine import get_db
from .users import Users
from auth.token import get_current_user

class Posts(SQLModel, table=True):
    __name__ = "posts"

    id:Annotated[Optional[int], Field(default=None, primary_key=True)]
    username:Annotated[str, Field(foreign_key="users.username")]
    parent_post:Annotated[int|None, Field(default=None)]
    created_at:Annotated[Optional[datetime], Field(sa_column_kwargs={"server_default": func.now()})]
    content:Annotated[str, Field(nullable=False)]
    likes:Annotated[int, Field(default=0)] 

class UserPostsJoin(BaseModel):
    username:str
    name:str
    content:str
    likes:int
    created_at:datetime

def create_post(
        user:Annotated[Users, Depends(get_current_user)], 
        db:Annotated[Session, Depends(get_db)],
        content:str
        ):
    
    new_post = Posts(
        username = user.username,
        content = content
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

def get_user_posts(username:str, db:Annotated[Session, Depends(get_db)]):
    query = select(Posts).query = select(Posts, Users).join(Users, Users.username == Posts.username).where(Posts.username == username)
    posts = db.exec(query).all()
    return posts

def get_posts_by_date(db:Annotated[Session, Depends(get_db)]):
    query = select(Posts, Users).join(Users, Users.username == Posts.username).order_by(desc(Posts.created_at))
    posts = db.exec(query).all()

    return posts