from databases import Database
from sqlalchemy import MetaData, create_engine

DATABASE_URL = "sqlite:///./dev.db"

# async Database (used by application code)
database = Database(DATABASE_URL)

# SQLAlchemy metadata and engine (used to create tables)
metadata = MetaData()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
