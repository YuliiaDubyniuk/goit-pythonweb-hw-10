from datetime import date
from sqlalchemy import Date, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
    )
    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )
    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    avatar: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )
    verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )


class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
    ForeignKey("users.id"),
    nullable=False,
    )
    first_name: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )
    last_name: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )
    phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    birth_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
    additional_data: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
