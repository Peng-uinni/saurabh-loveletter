from fastapi import FastAPI, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, HTMLResponse

from routers import users, posts, home
from database.engine import create_db_and_tables
from pages.templating import templates

app = FastAPI()
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(home.router)

app.mount("/css", StaticFiles(directory="./pages/css"), name="css")

@app.on_event("startup")
def startup():
    create_db_and_tables()