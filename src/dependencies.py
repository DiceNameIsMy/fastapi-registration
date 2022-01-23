from repository import Repository, get_repository_class


repository_class = get_repository_class()


def get_repository() -> Repository:
    repository = repository_class()
    try:
        yield repository
    finally:
        repository.commit()
        repository.close_connection()
