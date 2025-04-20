from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
from typing import Annotated

from pages.templating import templates
from database.engine import get_db, Session
from database.posts import create_post
from database.users import Users
from auth.token import get_current_user

router = APIRouter(prefix="/posts")

#schema
class PostFormData(BaseModel):
    content:str

#endpoints
@router.get("/create", response_class=HTMLResponse)
async def new_post_page(
    request:Request,
    user:Annotated[Users, Depends(get_current_user)]
    ):
    return templates.get_template(name="create_post.html", request=request)

@router.post("/create")
async def new_post(
    db:Annotated[Session, Depends(get_db)],
    form_data:Annotated[PostFormData, Form()],
    user:Annotated[Users, Depends(get_current_user)]
):
    create_post(user, db, form_data.content)
    return RedirectResponse(url="/", status_code=302)