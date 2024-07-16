import enum

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import ENUM


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String(254), unique=True, )
    password = Column(String)
    active = Column(Boolean, default=True)


class UserRoleEnum(enum.Enum):
    admin = "admin"
    moderator = "moderator"
    user = "user"


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    key = Column(Integer, ForeignKey('users.id'))
    role = Column(ENUM(UserRoleEnum), nullable=False)
