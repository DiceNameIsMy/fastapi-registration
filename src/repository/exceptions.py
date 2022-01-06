class RepositoryError(Exception):
    pass


class IntegrityError(RepositoryError):
    """Called when unique constraint was violated"""

    def __init__(
        self,
        fields: list[str],
        message: str = "One or more of the provided fields ({}) already exist",
    ) -> None:
        self.message = message.format(", ".join(fields))

        super().__init__(self.message)


class DoesNotExistError(RepositoryError):
    """Called when no model matching to a query was found"""

    def __init__(
        self, model, message: str = "{} matching to a query does not exist"
    ) -> None:
        self.message = message.format(model)
        super().__init__(self.message)
