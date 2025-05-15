from fastapi import APIRouter

router = APIRouter()

@router.get("/ping", tags=["Health Check"])
async def ping():
    return {"message": "pong"}