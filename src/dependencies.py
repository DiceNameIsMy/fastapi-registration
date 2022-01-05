from sqlalchemy.orm.session import Session

from repository.database import SessionLocal
from repository import BaseRepository, get_repository


repository_class = get_repository()


def get_repository() -> BaseRepository:
    session: Session = SessionLocal()
    repository = repository_class(session)
    try:
        yield repository
    finally:
        repository.commit()
        repository.close_connection()
