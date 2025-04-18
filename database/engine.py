from sqlmodel import SQLModel, Session, create_engine

from . config import DB_USERNAME, DB_PASSWORD, HOST, PORT, DATABASE

DB_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{HOST}:{PORT}/{DATABASE}"
engine = create_engine(DB_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_db():
    with Session(engine) as session:
        yield session
