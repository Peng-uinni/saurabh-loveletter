from pydantic import BaseModel
    
class PageContext(BaseModel):
    title:str
    link_field:list
    username:str
    name:str
    posts:list


def null_context() -> PageContext:
    context = PageContext(
        title = "null",
        link_field = ["Nothing here"],
        username = "",
        name = "",
        posts = []
    )

    return context