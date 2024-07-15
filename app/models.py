import datetime
from typing import Annotated

from sqlalchemy import (
    DateTime,
    ForeignKey,
    MetaData
)
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

intpk = Annotated[int, mapped_column(primary_key=True)]


class Users(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    name: Mapped[str]
    login: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    role: Mapped[int] = mapped_column(ForeignKey("roles_list.id", ondelete="CASCADE"))


class Roles(Base):
    __tablename__ = "roles_list"

    id: Mapped[intpk]
    role: Mapped[str] = mapped_column(unique=True)


class ScrapList(Base):
    __tablename__ = "scrap_list"

    id: Mapped[intpk]
    name: Mapped[int] = mapped_column(ForeignKey("name_list.id", ondelete="CASCADE"))
    weight: Mapped[float] = mapped_column(nullable=True)
    price: Mapped[float]
    percent_nds: Mapped[float]
    edit_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    editor: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)


class NameList(Base):
    __tablename__ = "name_list"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(unique=True)
