from fastapi import APIRouter, Depends

from sqlalchemy.orm.session import Session

from dependencies import get_db_session

from domain.user import UserDomain
from domain.user.schemes import UserRepr
from settings import settings


router = APIRouter(
    prefix="/api/v1",
)

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.get("", response_model=list[UserRepr])
def get_users(
    session: Session = Depends(get_db_session),
    page: int = 0,
    page_size: int = settings.page_size,
):
    domain = UserDomain(session)
    return domain.get_users(page=page, page_size=page_size)


router.include_router(users_router)
