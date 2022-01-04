from sqlalchemy.orm.session import Session

from repository.database import SessionLocal
from repository import Repository


def get_repository():
    session: Session = SessionLocal()
    repository = Repository(session)
    try:
        yield repository
    finally:
        repository.commit()
        repository.close_connection()
