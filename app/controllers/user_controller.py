from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm.session import Session
from typing import List

from app.domain.config import *
from app.domain.constants import *
from app.domain.database import get_db
from app.auth.bearer import BearerAuth
from app.dtos import user_dtos
from app.dtos import error
from app.exceptions.app_exceptions import NotFoundException, UnauthorizedRequestException
from app.mappings.user_mappings import *
from app.services import auth_service, jwt_service, user_service


controller = APIRouter(
    prefix=USERS_URL,
    tags=["Users"]
)


@controller.post(
    path="",
    status_code=200,
    responses={
        200: {
            "model": user_dtos.UserResponse
        },
        400: {
            "model": error.ErrorResponse
        },
        422: {
            "model": error.ValidationErrorResponse
        }
    }
)
async def register(
    user_data: user_dtos.UserCreate,
    db: Session = Depends(get_db)
):
    """Create new user"""

    new_user = user_service.create_user(db, user_data)
    return new_user


@controller.post(
    path="/login",
    status_code=200,
    responses={
        200: {
            "model": user_dtos.Token
        },
        401: {
            "model": error.ErrorResponse
        },
        422: {
            "model": error.ValidationErrorResponse
        }
    }
)
async def login(
    login_data: user_dtos.Login,
    db: Session = Depends(get_db)
):
    """Generate access token for valid credentials"""

    if not auth_service.authenticate_user(db, login_data.email, login_data.password):
        raise UnauthorizedRequestException("Incorrect email or password")

    create_token_data = login_to_create_token(login_data)
    token = jwt_service.create_access_token(create_token_data)

    return token


@controller.post(
    path="/externallogin",
    status_code=200,
    responses={
        200: {
            "model": user_dtos.Token
        },
        422: {
            "model": error.ValidationErrorResponse
        }
    }
)
async def external_login(
    external_login_data: user_dtos.ExternalLogin,
    db: Session = Depends(get_db)
):
    """Generate access token for valid credentials for social login"""

    user = user_service.get_user_by_email(db, external_login_data.email)

    if not user:
        user_service.create_social_user(db, external_login_data)

    create_token_data = external_login_to_create_token(external_login_data)
    token = jwt_service.create_access_token(create_token_data)

    return token


@controller.post(
    path="/forgotpassword",
    status_code=204,
    responses={
        204: {},
        404: {
            "model": error.ErrorResponse
        },
        422: {
            "model": error.ValidationErrorResponse
        }
    }
)
async def forgot_password(
    reset_password_data: user_dtos.ResetPassword,
    db: Session = Depends(get_db)
):
    """Generate password reset link"""
    user = user_service.get_user_by_email(db, reset_password_data.email)

    if not user:
        raise NotFoundException(message=f"User with email: {reset_password_data.email} does not exist")

    user_service.forgot_password(db, user)


@controller.get(
    path="",
    dependencies=[Depends(BearerAuth())],
    status_code=200,
    responses={
        200: {
            "model": List[user_dtos.UserResponse]
        },
        401: {
            "model": error.ErrorResponse
        },
        403: {
            "model": error.ErrorResponse
        }
    }
)
async def get_all(
    request: Request,
    db: Session = Depends(get_db)
):
    """Get user"""

    users = user_service.get_users(db, request)
    return users


@controller.get(
    path="/{id}",
    dependencies=[Depends(BearerAuth())],
    status_code=200,
    responses={
        200: {
            "model": user_dtos.UserResponse
        },
        401: {
            "model": error.ErrorResponse
        },
        403: {
            "model": error.ErrorResponse
        },
        404: {
            "model": error.ErrorResponse
        }
    }
)
async def get(
    id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """Get user"""

    user = user_service.get_user(db, id, request)
    return user


@controller.put(
    path="/{id}",
    dependencies=[Depends(BearerAuth())],
    status_code=200,
    responses={
        200: {
            "model": user_dtos.UserResponse
        },
        400: {
            "model": error.ErrorResponse
        },
        401: {
            "model": error.ErrorResponse
        },
        404: {
            "model": error.ErrorResponse
        },
        422: {
            "model": error.ValidationErrorResponse
        }
    }
)
async def update(
    id: int,
    user_data: user_dtos.UserUpdate,
    request: Request,
    db: Session = Depends(get_db)
):
    """Update user"""

    user = user_service.get_user_by_id(db, id)

    if not user:
        raise NotFoundException(f"User with id: {id} does not exist")

    updated_user = user_service.update_user(db, id, request, user_data)
    return updated_user


@controller.put(
    path="/{id}/adminstatus",
    dependencies=[Depends(BearerAuth())],
    status_code=200,
    responses={
        200: {
            "model": user_dtos.UserResponse
        },
        400: {
            "model": error.ErrorResponse
        },
        401: {
            "model": error.ErrorResponse
        },
        404: {
            "model": error.ErrorResponse
        },
        422: {
            "model": error.ValidationErrorResponse
        }
    }
)
async def change_admin_status(
    id: int,
    user_admin_status: user_dtos.UserAdminStatus,
    request: Request,
    db: Session = Depends(get_db)
):
    """Update user admin status"""

    user = user_service.get_user_by_id(db, id)

    if not user:
        raise NotFoundException(message=f"User with id: {id} does not exist")

    updated_user = user_service.change_user_admin_status(db, id, user_admin_status, request)
    return updated_user
