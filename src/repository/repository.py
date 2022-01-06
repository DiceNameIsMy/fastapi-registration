from abc import ABC
from typing import Type

from sqlalchemy.orm.session import Session

from settings import settings

from .database import SessionLocal
from .models import UserModel
from .schemes import User, CreateUser


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
        # TODO catch unique violataion
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
        user = self.session.query(UserModel).get(id=user_id)
        return User.from_orm(user)

    def commit(self):
        self.session.commit()

    def close_connection(self):
        self.session.close()


fake_database = {"users": []}


class FakeRepository(BaseRepository):
    def __init__(self) -> None:
        self.db = fake_database

    def create_user(self, new_user: CreateUser, commit: bool) -> User:
        user = new_user.dict_to_create()
        user["id"] = self._get_next_user_id()
        self.db["users"].append(user)
        return User(**user)

    def get_users(self, page: int, page_size: int) -> list[User]:
        users = self.db["users"][page * page_size: page_size]
        return [User(**user) for user in users]

    def get_user_by_id(self, user_id) -> User:
        for user in self.db["users"]:
            if user["id"] == user_id:
                return User(**user)

    def _get_next_user_id(self):
        try:
            return self.db["users"][-1]["id"] + 1
        except IndexError:
            return 1

    def commit(self) -> None:
        pass

    def close_connection(self) -> None:
        pass


def get_repository_class() -> Type[BaseRepository]:
    if settings.db.fake:
        return FakeRepository

    return Repository
