# Python Microservice

## Project Structure

```bash
app/
├── main.py                 # Application entry point
├── api/
│   ├── __init__.py
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── endpoints/
│   │   │   ├── __init__.py
│   │   │   ├── health.py
│   │   │   └── users.py
│   │   └── router.py
├── core/
│   ├── __init__.py
│   ├── config.py           # Settings / env vars
│   ├── logging.py
│   └── security.py
├── models/
│   ├── __init__.py
│   └── user.py             # ORM models
├── schemas/
│   ├── __init__.py
│   └── user.py             # Pydantic models
├── services/
│   ├── __init__.py
│   └── user_service.py     # Business logic
├── db/
│   ├── __init__.py
│   ├── session.py
│   └── base.py
├── dependencies/
│   ├── __init__.py
│   └── auth.py
├── tests/
│   ├── __init__.py
│   └── test_users.py
└── __init__.py

Dockerfile
docker-compose.yml
pyproject.toml / requirements.txt
.env
```

