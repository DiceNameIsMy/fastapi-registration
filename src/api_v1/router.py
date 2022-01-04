from fastapi import APIRouter, Depends

from domain.user import UserDomain
from domain.dependencies import get_user_domain

from repository.schemes import CreateUser, UserRepr, PaginatedUsers

from settings import settings


router = APIRouter(
    prefix="/api/v1",
)

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.get("", response_model=PaginatedUsers)
def get_users(
    page: int = 0,
    page_size: int = settings.page_size,
    user_domain: UserDomain = Depends(get_user_domain),
):
    return user_domain.get_paginated_users(page=page, page_size=page_size)


@users_router.post("", response_model=UserRepr)
def create_user(
    new_user: CreateUser,
    user_domain: UserDomain = Depends(get_user_domain),
):
    return user_domain.create_user(new_user=new_user, commit=True)


router.include_router(users_router)
