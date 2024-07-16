import enum

from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import ENUM


class Base(DeclarativeBase):
    pass


class UserRoleEnum(enum.Enum):
    admin = "admin"
    user = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String(254), unique=True)
    password = Column(String)
    active = Column(Boolean, default=True)

    roles = relationship("Role", back_populates="user", cascade="all, delete-orphan")


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String)
    role = Column(Enum(UserRoleEnum), nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="roles")
