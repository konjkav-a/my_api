from fastapi import APIRouter, Depends, status
from .schemas import UserCreateModel, UserModel, UserLoginModel
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from src.db.engine import get_session
from .service import UserService
from .utils import create_access_token, decode_token, verify_password
from fastapi.responses import JSONResponse
from datetime import timedelta

auth_router = APIRouter()
user_service = UserService()


REFRESH_TOKEN_EXPIRY = 2

@auth_router.post('/signup', response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create_user_account(user_date: UserCreateModel, session: AsyncSession = Depends(get_session) ) :

    email = user_date.email
    user_exists = await user_service.user_exists(email, session)

    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="email already exist")

    new_user = await user_service.create_user(user_date, session)

    return new_user

@auth_router.post('/login')
async def login_user(user_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    email = user_data.email
    password = user_data.password
    user = await user_service.get_user_by_email(email, session)

    if user is not None:

        password_valid = verify_password(password, user.password_hash)

        if password_valid:
            access_token = create_access_token(user_data={
                                                        'email': user.email,
                                                        'user_uid': str(user.uid)
            })

            refresh_token = create_access_token(
                user_data = {'email': user.email,'user_uid': str(user.uid)},
                refresh = True,
                expiry = timedelta(days=REFRESH_TOKEN_EXPIRY))

            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "email": user.email,
                        "uid": str(user.uid)
                    }
                })

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Email Or Password")