from fastapi import Request
from fastapi.security.http import HTTPBearer
from app.domain.database import SessionLocal

from app.exceptions.app_exceptions import UnauthorizedRequestException
from app.services import auth_service


class BearerAuth(HTTPBearer):

    def __init__(self, auto_error: bool = False):
        super().__init__(auto_error=auto_error)
        self.db = SessionLocal()

    async def __call__(self, request: Request):
        scheme, token = request.headers.get("Authorization").split(" ")

        if not scheme or not token:
            raise UnauthorizedRequestException("Missing or malformed authorization header")

        if scheme.lower() != "bearer":
            raise UnauthorizedRequestException("Invalid authentication scheme")

        if not auth_service.verify_jwt(self.db, token):
            raise UnauthorizedRequestException("Invalid or expired token")

        return True
