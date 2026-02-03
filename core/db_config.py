from sqlalchemy import create_engine

url = 'postgresql+psycopg2://postgres:1811@postgres:5432/postgres'
engine = create_engine(url)
