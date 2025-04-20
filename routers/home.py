from fastapi import APIRouter, Request, Depends
from typing import Annotated

from pages.templating import templates, context
from database.engine import get_db, Session
from database.posts import get_posts_by_date
from auth.token import user_logged_in, get_current_user, Users

router = APIRouter(prefix="/home")

@router.get("")
async def home(
    request:Request,
    db:Annotated[Session, Depends(get_db)]
    ):

    _posts = get_posts_by_date(db)

    con = context.null_context()
    con.posts = _posts
    con.title = "Home"
    con.link_field = ["login", "signup"]

    return templates.get_template(name="home.html", request=request, context=con.model_dump())