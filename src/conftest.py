import contextlib
import pytest

from sqlalchemy import MetaData

from fastapi.testclient import TestClient

from repository.database import SessionLocal, Base
from repository import schemes, Repository, get_repository_class

from main import app


meta = MetaData()


@pytest.fixture(autouse=True)
def teardown():
    """Clears out database after each test."""
    yield

    with contextlib.closing(SessionLocal()) as con:
        trans = con.begin()
        con.execute(
            "TRUNCATE {} RESTART IDENTITY;".format(
                ",".join(
                    table.name
                    for table in reversed(Base.metadata.sorted_tables)
                )
            )
        )
        trans.commit()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def repository() -> Repository:
    return get_repository_class()()


@pytest.fixture
def user_with_email(repository: Repository) -> schemes.User:
    user = schemes.CreateUser(
        email="test@test.com",
        password1="password",
        password2="password",
    )
    return repository.create_user(user, commit=True)
