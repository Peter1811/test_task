from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from core.db_config import engine
from models.base_models import Base
from models.models import TestModel


app = FastAPI()

Base.metadata.create_all(engine)


@app.get('/')
async def main_page():
    with Session(engine) as session:
        new_test_model = TestModel(name='first_model')
        session.add(new_test_model)
        session.commit()

    return PlainTextResponse('this is main page')

@app.get('/test')
async def test():
    return PlainTextResponse('this is test page')
