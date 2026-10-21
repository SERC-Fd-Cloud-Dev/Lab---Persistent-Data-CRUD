# Movie Clue Game API homework

**Core time: approximately 60 minutes.** Transfer your persistence skills to a new
scenario. The frontend, clue text, answer checking helper, request schemas, engine
and Alembic environment are supplied. You implement the model, migration and two
API handlers. The core game works without caching. No external movie API is needed.

## Start 5 minutes

Use Python 3.11/3.12. Create and activate a virtual environment in this repository
(macOS/Linux: `source .venv/bin/activate`; PowerShell: `.venv\Scripts\Activate.ps1`).
If activation is blocked, call the environment's Python executable directly.

```bash
python -m venv .venv
python -m pip install -r requirements-lock.txt
python -m pytest tests/test_setup.py -q
python -m uvicorn app.main:app --reload
```

Open <http://127.0.0.1:8000/> and <http://127.0.0.1:8000/docs>.
Serve the supplied frontend through FastAPI; do not open the HTML with file://.
Both use the same origin, so no CORS configuration is required.
At the start the interface loads, but submitting a guess shows an API error until
you implement the handlers. That is the intended starting state.

## Model and migration 15 minutes

In `app/models.py`, keep the supplied primary key and implement the mapped fields:

| Field | Type | Meaning |
|---|---|---|
| id | Integer primary key | Generated attempt identity |
| player | String(40), required | Exact nickname, use made-up names |
| clue_id | Integer, required | Supplied clue identity |
| title | String(120), required | Submitted movie title |
| correct | Boolean, required | Server's decision |

Recall the classroom mapped-column pattern. Check `String`, `Boolean`, `Mapped`
and `mapped_column` imports before implementing. Generate a migration with
`python -m alembic revision --autogenerate -m "create guesses"`, review the candidate,
then run `python -m alembic upgrade head` and `python -m alembic current`.
Editing a model alone does not change an existing database schema.

## Implement and connect 25 minutes

Work in `app/main.py`. Keep the supplied frontend, schemas and answer helper.

**Guided start:** read how the supplied handler rejects an unknown clue before
writing. Use `check_guess(data.clue_id, data.title)` for the Boolean result. Create
a Guess object from the request and result, add it, commit and refresh it. Reuse
the taught try/rollback pattern if a write fails. Return the saved object.

**Supported practice:** test `POST /guesses` in Swagger UI, then submit from the
frontend. If it fails, compare its JSON with the contract before changing the UI.

**Partially independent core finish:** implement the history query yourself.
Filter by exact `player`, order by id, return an array and keep histories separate.
No complete query is provided. Decide how to express the filter using the ORM
selection pattern you practised in class. An unknown player has an empty history.

| Request | Response |
|---|---|
| POST /guesses with `{"player":"Alex","clue_id":1,"title":"Toy Story"}` | 201 and `{"id":1,"player":"Alex","clue_id":1,"title":"Toy Story","correct":true}` |
| GET /guesses?player=Alex | 200 and array of that player's saved objects, oldest first |
| Unknown clue in POST | 404 and no stored attempt |

Ids may differ. Store the original title for display; use the helper's whitespace
and case-insensitive comparison for correctness. Answers stay in `app/answers.py`
on the server. The frontend contains clue text only. A nickname is a filter in this
local exercise, not authentication or proof of ownership.

## Verify 10 minutes

```bash
python -m pytest tests/test_setup.py tests/test_guesses.py -q
```

Then make one correct and one incorrect attempt through the frontend. Change
nickname and verify history separation. Stop the backend, restart the **same**
command from the **same repository root**, refresh history and confirm the attempts
remain. Keep the migration and database file locally; do not commit the database.
The tests use temporary databases, so test results do not alter your game history.

## Explain 5 minutes

Bring your working implementation, migration and test result to the review. In a
few sentences explain where attempts live, why a restart retains them and how a
Session commits an attempt. Identify one problem you diagnosed and how you checked
your correction. A long report is unnecessary.

## Optional stretch caching

After completing the core, cache GET history using the supplied dictionary. Key it
by the same exact player value used in your database filter. Cache plain lists of
response dictionaries, including empty histories. After a successfully committed
POST, invalidate that player's cached history. Set `X-Cache` to `miss` or `hit`.
Run `python -m pytest tests/test_cache_stretch.py -q`.
`python -m pytest -q` includes this optional test; failure of only this test does
not mean the core homework is incomplete. TTL and Redis are unnecessary.

## Hints and recovery

1. State whether the failure concerns an HTTP contract, database schema, transaction
   or query filter before editing code.
2. Compare model fields with the contract and check Alembic current.
3. For an empty history, check player spelling and whether POST committed.
4. For a later read missing data, check the SQLite URL and working directory.
5. If schema setup blocks you, show the exact migration/error to the lecturer.

Minimum catch-up: migrate the model, save one attempt and retrieve it after a
restart. Complete the history filter and core checks next. Stop with Ctrl+C.
No cloud resources, account, real personal details or paid service are required.
