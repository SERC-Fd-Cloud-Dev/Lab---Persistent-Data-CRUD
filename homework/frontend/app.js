const form = document.querySelector('#game');
const player = document.querySelector('#player');
const message = document.querySelector('#message');
const list = document.querySelector('#history');
const submit = document.querySelector('#submit');

async function request(url, options) {
  const response = await fetch(url, options);
  if (!response.ok) throw new Error(`API returned ${response.status}. Check your backend and /docs.`);
  return response.json();
}

async function refresh() {
  const rows = await request(`/guesses?player=${encodeURIComponent(player.value)}`);
  list.replaceChildren();
  for (const row of rows) {
    const li = document.createElement('li');
    li.textContent = `Clue ${row.clue_id}: ${row.title} — ${row.correct ? 'Correct' : 'Try again'}`;
    list.append(li);
  }
  if (!rows.length) {
    const li = document.createElement('li'); li.textContent = 'No saved attempts for this player.'; list.append(li);
  }
}

form.addEventListener('submit', async (event) => {
  event.preventDefault(); submit.disabled = true;
  try {
    const result = await request('/guesses', {method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({player: player.value, clue_id: Number(document.querySelector('#clue').value),
                            title: document.querySelector('#title').value})});
    message.textContent = result.correct ? 'Correct! Your attempt has been saved.' : 'Not this time. Your attempt has been saved.';
    await refresh();
  } catch (error) {message.textContent = error.message;}
  finally {submit.disabled = false;}
});
document.querySelector('#refresh').addEventListener('click', () => refresh().catch(error => message.textContent = error.message));
