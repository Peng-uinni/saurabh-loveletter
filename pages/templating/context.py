from pydantic import BaseModel
    
class UserPageContext(BaseModel):
    title:str
    link_field:str
    username:str
    name:str
    posts:list
