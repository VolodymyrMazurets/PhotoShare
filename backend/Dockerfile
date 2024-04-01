FROM python:3.12 AS builder

WORKDIR  /app

RUN python3 -m venv venv
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./pyproject.toml /app/pyproject.toml

RUN pip3 install poetry

RUN poetry install 

FROM python:3.12 AS runner
 
WORKDIR /app
 
COPY --from=builder /app/venv venv
COPY . .
 
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
 
EXPOSE 8000
 
CMD [ "poetry", "run", "uvicorn", "--host", "0.0.0.0", "src.main:app" ]
