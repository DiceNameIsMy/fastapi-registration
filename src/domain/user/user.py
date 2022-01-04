from repository import Repository
from repository.schemes import User, CreateUser, PaginatedUsers


class UserDomain:
    def __init__(self, repository: Repository) -> None:
        self.repository = repository

    def create_user(self, new_user: CreateUser, commit: bool = False) -> User:
        user = self.repository.create_user(new_user=new_user, commit=commit)
        return User.from_orm(user)

    def get_paginated_users(self, page: int, page_size: int) -> PaginatedUsers:
        users = self.repository.get_users(page=page, page_size=page_size)
        return PaginatedUsers(items=users, total=len(users))
