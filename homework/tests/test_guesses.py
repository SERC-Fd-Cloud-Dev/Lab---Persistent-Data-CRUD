def test_saved_result_and_history(client):
    response = client.post('/guesses', json={'player': 'Alex', 'clue_id': 1, 'title': ' toy story '})
    assert response.status_code == 201
    guess = response.json()
    assert isinstance(guess['id'], int) and guess['correct'] is True
    history = client.get('/guesses?player=Alex')
    assert history.status_code == 200 and history.json() == [guess]

def test_wrong_guess_and_separate_players(client):
    result = client.post('/guesses', json={'player': 'Sam', 'clue_id': 2, 'title': 'Jaws'})
    assert result.status_code == 201 and result.json()['correct'] is False
    assert client.get('/guesses?player=Sam').json()[0]['title'] == 'Jaws'
    assert client.get('/guesses?player=Other').json() == []

def test_unknown_clue_does_not_write(client):
    response = client.post('/guesses', json={'player': 'Alex', 'clue_id': 999, 'title': 'x'})
    assert response.status_code == 404
    assert client.get('/guesses?player=Alex').json() == []
