from fastapi.testclient import TestClient
from app.main import create_app

def test_health_and_contract():
    with TestClient(create_app()) as client:
        assert client.get('/health').json() == {'status': 'ok'}
        assert '/equipment/{equipment_id}' in client.get('/openapi.json').json()['paths']
