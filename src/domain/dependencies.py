from fastapi import Depends

from dependencies import get_repository

from repository import Repository

from .user import UserDomain


def get_user_domain(repository: Repository = Depends(get_repository)):
    return UserDomain(repository)
