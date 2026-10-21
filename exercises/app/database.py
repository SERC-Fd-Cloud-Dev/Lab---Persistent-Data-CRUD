import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

equipment_URL = os.getenv('equipment_URL', 'sqlite:///./equipment.db')
options = {'check_same_thread': False} if equipment_URL.startswith('sqlite') else {}
engine = create_engine(equipment_URL, connect_args=options,
                       echo=os.getenv('SQL_ECHO') == '1')
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

def get_session():
    # One Session per request. The engine is shared; the Session is not.
    with SessionLocal() as session:
        yield session
