Employee Management System API

A production-structured Employee Management System built 

using FastAPI, SQLAlchemy, and JWT Authentication.


JWT-based Authentication

Password hashing with bcrypt

Employee CRUD operations

Role-based structure ready

Layered architecture (Router → Service → Repository)

JSON structured logging

Environment-based configuration

SQLite database


app/
 ├── main.py                # Application entry point

 ├── core/                  # Core utilities

 │    ├── config.py         # Environment settings

 │    ├── database.py       # DB connection & session

 │    ├── security.py       # JWT & password hashing

 │    ├── logger.py         # JSON logger setup

 │    └── json_logging_middleware.py  # Request logging
 │
 ├── auth/                  # Authentication module

 │    ├── router.py         # Login endpoint

 │    ├── schema.py         # Auth schemas

 │    └── dependencies.py   # JWT validation dependency
 │
 └── employees/             # Employee module

      ├── model.py          # SQLAlchemy model

      ├── schema.py         # Pydantic validation

      ├── repository.py     # DB operations

      ├── service.py        # Business logic

      └── router.py         # Employee endpoints


<pre> ## 📁 Project Structure ``` app/ ├── main.py # Application entry point │ ├── core/ # Core utilities │ ├── config.py # Environment settings │ ├── database.py # DB connection & session │ ├── security.py # JWT & password hashing │ ├── logger.py # JSON logger setup │ └── json_logging_middleware.py # Request logging │ ├── auth/ # Authentication module │ ├── router.py # Login endpoint │ ├── schema.py # Auth schemas │ └── dependencies.py # JWT validation dependency │ └── employees/ # Employee module ├── model.py # SQLAlchemy model ├── schema.py # Pydantic validation ├── repository.py # DB operations ├── service.py # Business logic └── router.py # Employee endpoints ``` </pre>

