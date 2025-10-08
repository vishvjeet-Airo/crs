from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.auth import get_current_user, login_for_access_token
from app.schemas import Token, User

router = APIRouter()


@router.post("/login", response_model=Token, summary="Obtain JWT access token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    return await login_for_access_token(form_data)


@router.get("/get_current_user", response_model=User, summary="Get current user")
async def read_users_me(current_user: User = Depends(get_current_user)) -> User:
    return current_user
