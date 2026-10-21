import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

guesses_URL = os.getenv('guesses_URL', 'sqlite:///./guesses.db')
options = {'check_same_thread': False} if guesses_URL.startswith('sqlite') else {}
engine = create_engine(guesses_URL, connect_args=options,
                       echo=os.getenv('SQL_ECHO') == '1')
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

def get_session():
    # One Session per request. The engine is shared; the Session is not.
    with SessionLocal() as session:
        yield session
