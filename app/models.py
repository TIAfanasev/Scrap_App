import datetime
from typing import Annotated

from sqlalchemy import (
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

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
    name: Mapped[int] = mapped_column(ForeignKey("scrapname_list.id", ondelete="CASCADE"))
    name_link: Mapped["ScrapNameList"] = relationship(back_populates="scrap_link")
    weight: Mapped[float] = mapped_column(nullable=True)
    price: Mapped[float]
    percent_nds: Mapped[float]
    edit_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=False))
    editor: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)


class ScrapNameList(Base):
    __tablename__ = "scrapname_list"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(unique=True)
    scrap_link: Mapped["ScrapList"] = relationship(back_populates="name_link")
