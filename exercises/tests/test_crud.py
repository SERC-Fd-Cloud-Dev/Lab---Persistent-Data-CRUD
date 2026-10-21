def create(client, name='Camera'):
    response = client.post('/equipment', json={'name': name, 'category': 'media', 'location': 'A1'})
    assert response.status_code == 201
    return response.json()

def test_create_read_and_list(client):
    item = create(client)
    assert isinstance(item['id'], int)
    assert client.get(f"/equipment/{item['id']}").json() == item
    assert item in client.get('/equipment').json()

def test_replace_and_delete(client):
    item = create(client)
    url = f"/equipment/{item['id']}"
    updated = client.put(url, json={'name': 'Tripod', 'category': 'media', 'location': None})
    assert updated.status_code == 200
    assert updated.json()['name'] == 'Tripod'
    assert client.get(url).json()['name'] == 'Tripod'
    deleted = client.delete(url)
    assert deleted.status_code == 204 and deleted.content == b''
    assert client.get(url).status_code == 404

def test_missing_records(client):
    assert client.get('/equipment/99999').status_code == 404
    assert client.put('/equipment/99999', json={'name': 'x', 'category': 'y'}).status_code == 404
    assert client.delete('/equipment/99999').status_code == 404

def test_student_write_then_read(client):
    # Complete this core check: create YOUR different record, then GET its id.
    # Assert the POST status, generated id and a field returned by a later read.
    raise NotImplementedError('Write your own isolated database integration check')
