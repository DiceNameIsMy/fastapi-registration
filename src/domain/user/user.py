from sqlalchemy.orm.session import Session

from settings import settings

from repository.models import UserModel

from .schemes import User, UserRepr, CreateUser


class UserDomain:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_user(self, new_user: CreateUser, commit: bool = False) -> User:
        user = UserModel(new_user.dict())
        self.session.add(user)
        if commit:
            self._commit()

        return User.from_orm(user)

    def get_users(
        self, page: int = 0, page_size: int = settings.page_size
    ) -> list[UserRepr]:
        users = (
            self.session.query(UserModel)
            .limit(page_size)
            .offset(page * page_size)
            .all()
        )
        return [UserRepr.from_orm(user) for user in users]

    def _commit(self):
        self.session.commit()
