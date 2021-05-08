from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm.session import Session
from typing import List

from app.auth.bearer import BearerAuth
from app.domain.constants import *
from app.domain.database import get_db
from app.dtos import error
from app.dtos import game_dtos
from app.services import game_service

controller = APIRouter(
    prefix=GAMES_URL,
    tags=["Games"]
)


@controller.post(
    path="",
    dependencies=[Depends(BearerAuth())],
    status_code=200,
    responses={
        200: {
            "model": game_dtos.GameResponse
        },
        401: {
            "model": error.ErrorResponse
        },
        422: {
            "model": error.ValidationErrorResponse
        }
    }
)
async def create(
    game_data: game_dtos.GameCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """Create new game"""

    new_game = game_service.create_game(db, request, game_data)
    return new_game


@controller.get(
    path="",
    dependencies=[Depends(BearerAuth())],
    status_code=200,
    responses={
        200: {
            "model": List[game_dtos.GameResponse]
        },
        401: {
            "model": error.ErrorResponse
        }
    }
)
async def get_all(
    request: Request,
    db: Session = Depends(get_db)
):
    """Get games"""

    games = game_service.get_games(db, request)
    return games


@controller.get(
    path="/leaderboard",
    dependencies=[Depends(BearerAuth())],
    status_code=200,
    responses={
        200: {
            "model": List[game_dtos.GameResponse]
        },
        401: {
            "model": error.ErrorResponse
        }
    }
)
async def leaderboard(
    db: Session = Depends(get_db)
):
    """Get weekly leaderboard"""

    leaderboard = game_service.get_leaderboard(db)
    return leaderboard


@controller.get(
    path="/{id}",
    dependencies=[Depends(BearerAuth())],
    status_code=200,
    responses={
        200: {
            "model": game_dtos.GameResponse
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
    """Get game"""

    game = game_service.get_game(db, id, request)
    return game
