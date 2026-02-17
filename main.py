from fastapi import FastAPI, Body, Depends, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List

from core.db_config import engine
from models.base_models import Base
from models.models import Account, User
from schemas.schemas import CreateUser, GetAccount, GetUser


app = FastAPI()

Base.metadata.create_all(engine)


@app.get('/')
async def main_page():
    return PlainTextResponse('this is main page')


@app.post('/register', response_model=CreateUser)
async def register(user_data: CreateUser):
    '''
    Регистрация нового пользователя
    '''

    with Session(engine) as session:
        query = select(User).where(User.email==user_data.email)
        existing_user = session.scalars(query).first()
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail=f'user with email {user_data.email} already exists'
            )

        new_user = User(
            email=user_data.email,
            hash_password=hash(user_data.password),
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )
        session.add(new_user)
        session.commit()

    return user_data


@app.get('/users/', response_model=List[GetUser])
async def get_users_list():
    '''
    Получение списка пользователей
    '''

    with Session(engine) as session:
        users = session.query(User).all()
        if not users:
            raise HTTPException(
                status_code=400,
                detail=f'no users yet'
            )
        
        return_users = [
            GetUser(
                id=user.id,
                email=user.email,
                full_name=user.first_name + ' ' + user.last_name,
                accounts_id = [
                    account.id
                    for account in user.accounts
                ]
            )
            for user in users
        ]
        
    return return_users


@app.get('/users/{user_id}', response_model=GetUser)
async def get_user_info(user_id: int):
    '''
    Получение данных о пользователе по его id
    '''

    with Session(engine) as session:
        curr_user: User | None = session.query(User).get(user_id)
        
        if not curr_user:
            raise HTTPException(
                status_code=400,
                detail=f'there is not user with id {user_id}'
            )

        accounts = [
            account.id
            for account in curr_user.accounts
        ]

    user_data = GetUser(
        id=curr_user.id,
        email=curr_user.email,
        full_name=curr_user.first_name + ' ' + curr_user.last_name,
        accounts_id=accounts
    )

    return user_data


@app.post('/create-account/{user_id}', response_model=GetAccount)
async def create_account(user_id: int):
    '''
    Создание счета (изначально нулевой баланс)
    '''

    with Session(engine) as session:
        curr_user: User | None = session.query(User).get(user_id)

        if not curr_user:
            raise HTTPException(
                status_code=400,
                detail=f'there is not user with id {user_id}'
            )
        
        new_account = Account(
            user=curr_user    
        )

        session.add(new_account)
        session.commit()

        connected_user_id = curr_user.id
        new_account_id = new_account.id

    return GetAccount(
        id=new_account_id,
        balance=0, 
        connected_user_id=connected_user_id
    )
