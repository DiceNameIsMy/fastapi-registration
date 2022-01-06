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
