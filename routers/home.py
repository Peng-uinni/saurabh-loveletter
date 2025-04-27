from fastapi import APIRouter, Request, Depends, Cookie
from typing import Annotated

from pages.templating import templates, context
from database.engine import get_db, Session
from database.posts import get_posts_by_date
from auth.token import user_logged_in

router = APIRouter()

@router.get("/")
async def home(
    request:Request,
    db:Annotated[Session, Depends(get_db)],
    ):

    try:  
        access_token = request.cookies.get("access_token")
        logged_in = await user_logged_in(access_token)
    except Exception:
        logged_in = False

    _posts = get_posts_by_date(db)

    con = context.null_context()
    con.posts = _posts
    con.title = "Home"  
    
    if logged_in:
        con.link_field = ["home-login"]
        con.logged_in = True 
    else:
        con.link_field = ["home-no-login"]

    return templates.get_template(name="home.html", request=request, context=con.model_dump())