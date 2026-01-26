from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from helpers.transactions import Base
from helpers.config import Config

# Create SQLite database engine
DATABASE_URL = Config.get_database_url()

# Create session factory
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def init_db():
    """Create all tables in the database."""
    Base.metadata.create_all(bind=engine)


def get_session():
    """Get a new database session."""
    return SessionLocal()
