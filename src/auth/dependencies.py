from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi import Request, status
from .utils import decode_token
from fastapi.exceptions import HTTPException

class AccessToken(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        token = creds.credentials

        token_data = decode_token(token)

        if token_data is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid or expired token")

        if token_data['refresh']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail = "Invalid or expired token")

        return token_data

