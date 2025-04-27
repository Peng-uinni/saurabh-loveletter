from pydantic import BaseModel
    
class PageContext(BaseModel):
    title:str
    link_field:list
    username:str
    name:str
    posts:list
    logged_in:bool


def null_context() -> PageContext:
    context = PageContext(
        title = "null",
        link_field = [""],
        username = "",
        name = "",
        posts = [],
        logged_in = False
    )

    return context