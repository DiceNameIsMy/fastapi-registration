from repository import Repository
from repository.schemes import User, UserRepr, CreateUser, PaginatedUsers


class UserDomain:
    def __init__(self, repository: Repository) -> None:
        self.repository = repository

    def create_user(self, new_user: CreateUser) -> User:
        user = self.repository.create_user(new_user=new_user, commit=True)
        return User.from_orm(user)

    def get_user_by_id(self, user_id: int) -> User:
        return User.from_orm(self.repository.get_user_by_id(user_id))

    def update_user(self, user_id: int, updated_user: UserRepr) -> User:
        user = self.repository.get_user_by_id(user_id)
        self.repository.update_user(user, updated_user, commit=True)
        return user

    def get_paginated_users(self, page: int, page_size: int) -> PaginatedUsers:
        users = self.repository.get_users(page=page, page_size=page_size)
        return PaginatedUsers(items=users, total=len(users))
