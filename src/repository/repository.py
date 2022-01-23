from typing import Type

from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError as sa_IntegrityError

from settings import settings

from .database import SessionLocal
from .models import UserModel
from .schemes import CreateUser, UserRepr
from .exceptions import IntegrityError, DoesNotExistError


class Repository:
    def __init__(self) -> None:
        self.session: Session = SessionLocal()

    def create_user(
        self, new_user: CreateUser, commit: bool = True
    ) -> UserModel:
        user = UserModel(**new_user.dict_to_create())
        self.session.add(user)
        if commit:
            try:
                self.commit()
            except sa_IntegrityError:
                self.rollback()
                raise IntegrityError(["email", "phone"])

        return user

    def get_users(
        self, page: int = 0, page_size: int = settings.page_size
    ) -> list[UserModel]:
        return (
            self.session.query(UserModel)
            .limit(page_size)
            .offset(page * page_size)
            .all()
        )

    def get_user_by_id(self, user_id) -> UserModel:
        user = self.session.query(UserModel).get(user_id)
        if user is not None:
            return user
        else:
            raise DoesNotExistError(UserModel)

    def update_user(
        self, user: UserModel, updated_user: UserRepr, commit: bool = True
    ) -> bool:
        updated_data = updated_user.dict(exclude_defaults=True)
        for field in updated_data:
            setattr(user, field, updated_data[field])

        if commit:
            self.commit()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def close_connection(self):
        self.session.close()


def get_repository_class() -> Type[Repository]:
    return Repository
