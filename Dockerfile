FROM python:3.11

RUN apt-get update

WORKDIR /app
COPY . .

RUN python -m pip install --upgrade pip && pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]
