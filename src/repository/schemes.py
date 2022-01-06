from typing import Optional

from pydantic import BaseModel, root_validator


class _UserBase(BaseModel):
    phone: Optional[str] = None
    email: Optional[str] = None

    class Config:
        orm_mode = True


class User(_UserBase):
    id: Optional[int]
    password: str
    is_active: bool


class UserRepr(_UserBase):
    is_active: bool


class CreateUser(_UserBase):
    password1: str
    password2: str
    is_active: bool = True

    @property
    def password(self) -> str:
        return self.password1

    @root_validator(pre=True)
    def check_passwords_match(cls, values):
        if values["password1"] != values["password2"]:
            raise ValueError("Passwords do not match")
        if not any((values.get("email", None), values.get("phone", None))):
            raise ValueError("Email or Phone is required")
        return values

    def dict_to_create(self) -> dict:
        return self.dict(include={"email", "phone", "is_active"}) | {
            "password": self.password,
        }


class PaginatedUsers(BaseModel):
    items: list[UserRepr]
    total: int
