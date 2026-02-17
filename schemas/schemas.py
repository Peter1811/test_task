from pydantic import BaseModel

from typing import List


class CreateUser(BaseModel):
    email: str
    password: str

    first_name: str
    last_name: str


class GetUser(BaseModel):
    id: int
    email: str
    full_name: str

    accounts_id: List[int]


class GetAccount(BaseModel):
    id: int
    balance: int

    connected_user_id: int
