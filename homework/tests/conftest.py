from pathlib import Path
import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_session
from app.main import create_app

@pytest.fixture
def client(tmp_path):
    engine = create_engine('sqlite:///' + str(tmp_path / 'test.db'),
                           connect_args={'check_same_thread': False})
    cfg = Config(str(Path(__file__).resolve().parents[1] / 'alembic.ini'))
    with engine.connect() as connection:
        cfg.attributes['connection'] = connection
        command.upgrade(cfg, 'head')
    sessions = sessionmaker(bind=engine)
    def test_session():
        with sessions() as session:
            yield session
    app = create_app()
    app.dependency_overrides[get_session] = test_session
    with TestClient(app) as test_client:
        yield test_client
    engine.dispose()
