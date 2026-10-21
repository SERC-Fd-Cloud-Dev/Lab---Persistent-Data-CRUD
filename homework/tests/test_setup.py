from fastapi.testclient import TestClient
from app.main import create_app

def test_frontend_and_health():
    with TestClient(create_app()) as client:
        assert client.get('/health').status_code == 200
        assert 'Movie Clue Game' in client.get('/').text
        assert client.get('/static/app.js').status_code == 200
        assert 'ANSWERS' not in client.get('/static/app.js').text
