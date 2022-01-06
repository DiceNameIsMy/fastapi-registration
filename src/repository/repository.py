from abc import ABC
from typing import Type

from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError as sa_IntegrityError

from settings import settings

from .database import SessionLocal
from .models import UserModel
from .schemes import User, CreateUser
from .exceptions import IntegrityError, DoesNotExistError


class BaseRepository(ABC):
    def create_user(self, new_user: CreateUser, commit: bool) -> User:
        ...

    def get_users(self, page: int, page_size: int) -> list[User]:
        ...

    def get_user_by_id(self, user_id) -> User:
        ...

    def commit(self) -> None:
        ...

    def close_connection(self) -> None:
        ...


class Repository(BaseRepository):
    def __init__(self) -> None:
        self.session: Session = SessionLocal()

    def create_user(self, new_user: CreateUser, commit: bool = False) -> User:
        user = UserModel(**new_user.dict_to_create())
        self.session.add(user)
        if commit:
            self.commit()

        return User.from_orm(user)

    def get_users(
        self, page: int = 0, page_size: int = settings.page_size
    ) -> list[User]:
        users = (
            self.session.query(UserModel)
            .limit(page_size)
            .offset(page * page_size)
            .all()
        )
        return [User.from_orm(user) for user in users]

    def get_user_by_id(self, user_id) -> User:
        user = self.session.query(UserModel).get(user_id)
        if user is not None:
            return User.from_orm(user)
        else:
            raise DoesNotExistError(UserModel)

    def commit(self):
        try:
            self.session.commit()
        except sa_IntegrityError:
            self.session.rollback()
            raise IntegrityError(["email", "phone"])

    def close_connection(self):
        self.session.close()


def get_repository_class() -> Type[BaseRepository]:
    return Repository
