from fastapi import FastAPI

from routers import users
from database.engine import create_db_and_tables

app = FastAPI()
app.include_router(users.router)

@app.on_event("startup")
def startup():
    create_db_and_tables()

@app.get("/")
async def root():
    return {"root":"root?"}