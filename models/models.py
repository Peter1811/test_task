from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base_models import Base


class TestModel(Base):
    __tablename__ = "test_model"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))


class Account(Base):
    __tablename__ = 'bank_accounts'

    id: Mapped[int] = mapped_column(primary_key=True)
    balance: Mapped[int] = mapped_column(default=0)

    user_id: Mapped[int] = mapped_column(
        ForeignKey('base_users.id'), 
        nullable=False
    )
    user = relationship('User', back_populates='accounts')


class Payment(Base):
    __tablename__ = 'payments'

    id: Mapped[int] = mapped_column(primary_key=True)
    deposit: Mapped[int] = mapped_column()


class User(Base):
    __tablename__ = 'base_users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    hash_password: Mapped[str] = mapped_column()
    first_name: Mapped[str] = mapped_column(String(10))
    last_name: Mapped[str] = mapped_column(String(20))

    accounts = relationship('Account', back_populates='user')


class Admin(Base):
    __tablename__ = 'admin'

    id: Mapped[int] = mapped_column(primary_key=True)

    email: Mapped[str] = mapped_column(String(50), unique=True)
    hash_password: Mapped[str] = mapped_column()
