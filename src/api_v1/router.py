from fastapi import APIRouter, Depends

from domain.user import UserDomain
from domain.dependencies import get_user_domain

from repository.schemes import (
    CreateUser,
    UserRepr,
    UserProfile,
    PaginatedUsers,
)
from repository.exceptions import IntegrityError, DoesNotExistError

from settings import settings
from exceptions import NotFoundHTTPException, BadRequestHTTPException

router = APIRouter(
    prefix="/api/v1",
)

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.get("/", response_model=PaginatedUsers, status_code=200)
def get_users(
    page: int = 0,
    page_size: int = settings.page_size,
    user_domain: UserDomain = Depends(get_user_domain),
):
    return user_domain.get_paginated_users(page=page, page_size=page_size)


@users_router.post("/", response_model=UserRepr, status_code=201)
def create_user(
    new_user: CreateUser,
    user_domain: UserDomain = Depends(get_user_domain),
):
    try:
        return user_domain.create_user(new_user=new_user)
    except IntegrityError as e:
        raise BadRequestHTTPException(detail=e.message)


@users_router.get("/{user_id}/", response_model=UserRepr, status_code=200)
def get_user(
    user_id: int,
    user_domain: UserDomain = Depends(get_user_domain),
):
    try:
        return user_domain.get_user_by_id(user_id)
    except DoesNotExistError:
        raise NotFoundHTTPException()


@users_router.put("/{user_id}/", response_model=UserProfile, status_code=200)
def update_user(
    user_id: int,
    updated_user: UserRepr,
    user_domain: UserDomain = Depends(get_user_domain),
):
    try:
        return user_domain.update_user(
            user_id=user_id, updated_user=updated_user
        )
    except DoesNotExistError:
        raise NotFoundHTTPException()
    except IntegrityError as e:
        raise BadRequestHTTPException(detail=e.message)


router.include_router(users_router)
