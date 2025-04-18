from fastapi import Depends
from sqlmodel import SQLModel, Session, Field, select
from typing import Annotated, Union

from .engine import get_db
from auth.password import hash_pwd

class Users(SQLModel, table=True):
    username : Annotated[str, Field(primary_key=True)]
    name : Annotated[Union[str, None], Field(default=None)]
    email : Union[str, None]
    password : str

def get_user_data(db:Annotated[Session, Depends(get_db)], username: str) -> Users|None:
    statement = select(Users).where(Users.username == username)
    result = db.exec(statement)
    return result.first()
    
def create_user(db:Annotated[Session, Depends(get_db)], user_data:dict):
    user = Users(username=user_data["username"],
                 email=user_data["email"],
                 password=hash_pwd(user_data["password"]))
    db.add(user)
    db.commit()
    db.refresh(user)

