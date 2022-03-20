from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Auth APIs"])


@router.post("/login")
def login():
    return "login"
