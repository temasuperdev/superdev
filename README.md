# superdev

Минимальный каркас приложения на FastAPI с асинхронным SQLite (databases + SQLAlchemy).

Запуск (локально):

1. Установите зависимости:

```bash
python -m pip install -r requirements.txt
```

2. Запустите сервер:

```bash
uvicorn app.main:app --reload
```

3. Запустите тесты:

```bash
pytest -q
```

Структура добавленных файлов:

- `requirements.txt` — зависимости
- `app/database.py` — async `Database`, SQLAlchemy `metadata` и `engine`
- `app/models.py` — SQLAlchemy таблицы
- `app/schemas.py` — Pydantic схемы
- `app/crud.py` — простые async CRUD-операции
- `app/main.py` — FastAPI приложение и endpoints
- `tests/test_basic.py` — базовый тест
