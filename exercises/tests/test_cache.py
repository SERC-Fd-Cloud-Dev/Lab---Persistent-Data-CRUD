def test_cache_hit_and_invalidation(client):
    item = client.post('/equipment', json={'name': 'Screen', 'category': 'media'}).json()
    url = f"/equipment/{item['id']}"
    assert client.get(url).headers.get('X-Cache') == 'miss'
    assert client.get(url).headers.get('X-Cache') == 'hit'
    client.put(url, json={'name': 'New screen', 'category': 'media'})
    fresh = client.get(url)
    assert fresh.headers.get('X-Cache') == 'miss'
    assert fresh.json()['name'] == 'New screen'
    client.delete(url)
    assert client.get(url).status_code == 404
