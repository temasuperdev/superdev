import os
from databases import Database
from sqlalchemy import MetaData, create_engine

# Read DATABASE_URL from environment so tests and containers can override it
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./dev.db")

# async Database (used by application code)
database = Database(DATABASE_URL)

# SQLAlchemy metadata and engine (used to create tables)
metadata = MetaData()

# For SQLite we need `check_same_thread=False` in connect_args
if DATABASE_URL.startswith("sqlite:"):
	engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
	engine = create_engine(DATABASE_URL)
