from fastapi import Depends

from dependencies import get_repository

from repository import BaseRepository

from .user import UserDomain


def get_user_domain(repository: BaseRepository = Depends(get_repository)):
    return UserDomain(repository)
