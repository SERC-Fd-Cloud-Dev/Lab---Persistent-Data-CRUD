def test_history_cache_invalidates(client):
    assert client.get('/guesses?player=Alex').headers.get('X-Cache') == 'miss'
    assert client.get('/guesses?player=Alex').headers.get('X-Cache') == 'hit'
    client.post('/guesses', json={'player': 'Alex', 'clue_id': 1, 'title': 'Toy Story'})
    fresh = client.get('/guesses?player=Alex')
    assert fresh.headers.get('X-Cache') == 'miss' and len(fresh.json()) == 1
