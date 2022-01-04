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

    @property
    def password(self) -> str:
        return self.password1

    @root_validator(pre=True)
    def check_passwords_match(cls, values):
        if values["password1"] != values["password2"]:
            raise ValueError("Passwords do not match")
        return values
