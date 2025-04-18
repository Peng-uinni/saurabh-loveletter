from fastapi import Request
from fastapi.templating import Jinja2Templates

from typing import Union

templates = Jinja2Templates(directory="./pages/html")

def get_template(
        request:Request,
        name:str,
        context:Union[dict, None] = None
    ):
    if context is None:
        return templates.TemplateResponse(request=request, name=name)
    return templates.TemplateResponse(request=request, name=name, context=context)