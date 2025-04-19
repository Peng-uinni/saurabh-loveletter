from fastapi import APIRouter

router = APIRouter(prefix="/posts")

@router.get("/create")
async def create_page():
    pass

@router.post("/create")
async def create_post():
    pass