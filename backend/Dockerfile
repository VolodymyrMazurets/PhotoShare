FROM python:3.12

WORKDIR  /app

COPY ./pyproject.toml /app/pyproject.toml

RUN pip3 install poetry

RUN poetry config virtualenvs.create false

RUN poetry install 

COPY . .

CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "--port", "8000", "src.main:app", "--reload"]
