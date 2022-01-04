from sqlalchemy import Boolean, Column, Integer, String

from .database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(254), unique=True, nullable=True)
    phone = Column(String(15), unique=True, nullable=True)

    password = Column(String(254))
    is_active = Column(Boolean, default=True)
