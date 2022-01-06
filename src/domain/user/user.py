from repository import BaseRepository
from repository.schemes import User, CreateUser, PaginatedUsers


class UserDomain:
    def __init__(self, repository: BaseRepository) -> None:
        self.repository = repository

    def create_user(self, new_user: CreateUser) -> User:
        user = self.repository.create_user(new_user=new_user, commit=True)
        return User.from_orm(user)

    def get_user_by_id(self, user_id: int):
        try:
            return self.repository.get_user_by_id(user_id)
        except Exception as e:
            raise e

    def get_paginated_users(self, page: int, page_size: int) -> PaginatedUsers:
        users = self.repository.get_users(page=page, page_size=page_size)
        return PaginatedUsers(items=users, total=len(users))
