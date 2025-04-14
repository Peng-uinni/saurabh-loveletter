from fastapi import Depends
from sqlmodel import SQLModel, Session, Field, select
from pydantic import BaseModel
from typing import Annotated, Union

from .engine import get_db

class Users(SQLModel, table=True):
    username : Annotated[str, Field(primary_key=True)]
    name : Annotated[Union[str, None], Field(default=None)]
    email : Union[str, None]
    password : str

def get_user_data(username: str, db:Annotated[Session,Depends(get_db)]):
    statement = select(Users).where(Users.username == username)
    result = db.exec(statement)
    return result.first()
    
def create_user(user_data:dict, db:Annotated[Session, Depends(get_db)]):
    user = Users(username=user_data["username"],
                 email=user_data["email"],
                 password=user_data["password"])
    db.add(user)
    db.commit()
    db.refresh(user)
