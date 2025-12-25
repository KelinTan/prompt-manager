# Prompt Manager Backend

## Python

3.11 +

## Setup

```bash

cp .env.example .env ## Edit .env file,change your environment variables

vim alembic.ini ## Edit alembic.ini file, change sqlalchemy.url to your database url

pip install poetry==1.8.2

poetry install
```

## Migrate

```bash

poetry run alembic upgrade head
```

## Start

### Start Web
```bash

uvicorn src.main:app --reload --host 0.0.0.0 --port 8080

or

./start.sh

or

python src/main.py

```

## Style

```bash

poetry run black src/ test/
```

## Test
    
```bash

poetry run pytest
```

## Framework

- FastAPI
- Pydantic
- SQLModel
- aiomysql
- pyjwt
- OpenAI
- Dashscope
- alembic