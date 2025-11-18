# Pet-api

Запуск: poetry run pet-api

## Struct:
```
├── arithmetic
│   ├── s21_arithmetic.c
│   ├── s21_arithmetic.h
│   ├── s21_calc_complements.c
│   ├── s21_determinant.c
│   ├── s21_mult_matrix.c
│   ├── s21_mult_number.c
│   ├── s21_sub_matrix.c
│   └── s21_sum_matrix.c
├── coverage
│   ├── coverage.info
.

├── env
├── poetry.lock
├── pyproject.toml
├── README.md
├── src
│   ├── api
│   │   ├── auth.py
│   │   ├── books.py
│   │   ├── dependencies.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   │       ├── auth.cpython-313.pyc
│   │       ├── books.cpython-313.pyc
│   │       ├── dependencies.cpython-313.pyc
│   │       └── __init__.cpython-313.pyc
│   ├── core
│   │   ├── __pycache__
│   │   │   ├── security.cpython-313.pyc
│   │   │   └── settings.cpython-313.pyc
│   │   ├── security.py
│   │   └── settings.py
│   ├── database.py
│   ├── main.py
│   ├── models
│   │   ├── books.py
│   │   ├── __pycache__
│   │   │   ├── books.cpython-313.pyc
│   │   │   ├── refresh_tokens.cpython-313.pyc
│   │   │   └── users.cpython-313.pyc
│   │   ├── refresh_tokens.py
│   │   └── users.py
│   ├── __pycache__
│   │   ├── database.cpython-313.pyc
│   │   └── main.cpython-313.pyc
│   ├── schemas
│   │   ├── auth.py
│   │   ├── books.py
│   │   ├── __pycache__
│   │   │   ├── auth.cpython-313.pyc
│   │   │   ├── books.cpython-313.pyc
│   │   │   └── users.cpython-313.pyc
│   │   └── users.py
│   └── services
│       ├── auth.py
│       ├── books.py
│       ├── __pycache__
│       │   ├── auth.cpython-313.pyc
│       │   ├── books.cpython-313.pyc
│       │   ├── book_service.cpython-313.pyc
│       │   └── users.cpython-313.pyc
│       └── users.py
└── test