from fastapi import Depends
from sqlmodel import SQLModel, Session, Field, select
from typing import Annotated, Union, Optional

from .engine import get_db

class Posts(SQLModel, table=True):
    __name__ = "posts"

    id:Annotated[Optional[int], Field(default=None, primary_key=True)]
    username:Annotated[str, Field(primary_key=True, foreign_key="users.username")]
    parent_post:Annotated[str|None, Field(default=None)]
    content:Annotated[str, Field(nullable=False)]
    likes:int

def get_user_posts(username:str, db = Annotated[Session, Depends(get_db)]):
    query = select(Posts).where(username=username)
