# Lab Equipment Register API

Build a persistent API using SQLAlchemy, SQLite and Alembic. Compare explicit SQL
with ORM operations, implement CRUD routes and add a small local cache.
This repository is the complete exercise. Slides and lecturer narration are optional.

## Before you start

Use Python 3.11 or 3.12, a terminal and an editor. You should know Python classes,
functions, HTTP methods and basic FastAPI routes. Refresh primary keys and foreign
keys: a primary key identifies one row, while a foreign key refers to a row in
another table. The core implementation uses one equipment table. Sketch a possible
category-to-equipment one-to-many relationship, but do not build a second table.

### Install and check the starting state

Work in this repository's root. Python 3.12 was used for validation.

```bash
python -m venv .venv
```

Activate it on macOS/Linux with `source .venv/bin/activate`, or on PowerShell with
`.venv\Scripts\Activate.ps1`. If activation is blocked, use
`.venv\Scripts\python.exe` in place of `python` on Windows, or `.venv/bin/python`
on macOS/Linux. You do not need to change your computer's execution policy.

```bash
python -m pip install -r requirements-lock.txt
python -m pytest tests/test_setup.py -q
python -m uvicorn app.main:app --reload
```

Open <http://127.0.0.1:8000/docs>. `/health` returns `{"status":"ok"}`.
Stop the server with Ctrl+C before schema work. Use a second terminal for commands
if leaving the server running. Full CRUD/cache tests intentionally fail until you
implement the corresponding milestones. They are learning checks, not setup checks.

### Starting files and ownership

| Supplied and working | Your implementation |
|---|---|
| Engine, request session dependency, Alembic environment, schemas, health route | Model fields and two migrations |
| One worked POST route and create/save pattern | SQL update/delete, ORM read/update |
| Route signatures and contract tests | Data-access reads, PUT, DELETE and your integration test |
| Empty dictionary on application state | Cache-aside GET and write invalidation |

Use `app/models.py`, `app/repository.py`, `app/main.py`, `scripts/`, your generated
migration files and `test_student_write_then_read` in `tests/test_crud.py`.
Keep existing contract assertions. Make a Git commit at each successful milestone.

## Persistence implementation 95 minutes

### P1 Data model and first migration 20 minutes

First interpret the model: `Equipment(id, name, category)`. A category can describe
many pieces of equipment. The supplied single table keeps this exercise small.
Add required typed `name` and `category` columns in `app/models.py`.

The pattern `label: Mapped[str] = mapped_column(String(30))` maps a Python string
attribute to a string column. Reuse the pattern with the field names and lengths
specified in the TODO comments. `id` is already supplied as the primary key.

The engine manages connectivity. A `Session` tracks objects and transactions.
Each request gets a new Session from `get_session`; never make one global Session.

```bash
python -m alembic revision --autogenerate -m "create equipment"
```

Open the new Python file under `migrations/versions/`. Check that `upgrade()`
creates equipment with id, name and category, and that `downgrade()` reverses this
schema operation. Autogeneration proposes a change; you must review it.

```bash
python -m alembic upgrade head
python -m alembic current
python -m scripts.inspect_schema
```

**Check:** all three columns exist and a revision id prints. Do not add
`Base.metadata.create_all()` to application startup. Alembic owns this exercise's schema.

### P2 SQL statements in Python 15 minutes

Run `python -m scripts.sql_practice`. Read the supplied bound INSERT and SELECT.
`text()` represents explicit SQL. `:name` is a bound value; never join user input
into SQL with f-strings. `.mappings()` produces row mappings rather than ORM objects.

Complete the TODOs: UPDATE the returned row by its id, check the changed value,
then DELETE that practice row. Commit after writes. Use parameter dictionaries
for every value. **Evidence:** INSERT, SELECT, UPDATE and DELETE all run, and a
SELECT after deletion finds no row. Explain why `WHERE id = :id` matters.

### P3 ORM and transaction practice 25 minutes

Run `python -m scripts.orm_practice`. `add` tracks a new object, `commit` flushes
pending SQL and commits the transaction, and `refresh` loads current column values.
`flush` alone is not a commit. The `with` block closes the Session; it does not
automatically commit uncommitted work.

Complete retrieval and update using `session.get(Equipment, item.id)` and attribute
assignment. Commit, then query again in a new Session. Leave the row in the database.
Try changing a value without committing and closing the Session: the later Session
should still see the last committed value. Explain what rollback would discard.

Compare the two approaches on the **same** row. Parameterised SQL:

```python
row = session.execute(
    text('SELECT id, name FROM equipment WHERE id = :id'), {'id': chosen_id}
).mappings().first()
```

ORM: `item = session.get(Equipment, chosen_id)`. Explain mapping versus object.
Set `SQL_ECHO=1` in your terminal before running the ORM script to inspect generated
SQL. PowerShell: `$env:SQL_ECHO='1'`; macOS/Linux: `export SQL_ECHO=1`.
Set it back to `0` afterwards. A Session's identity map may satisfy repeated
primary-key lookups of an already-loaded object without another SELECT.

**Check:** a new Session sees the saved value. SQL and ORM both execute database
operations; neither is automatically faster. Query shape, indexes and loading matter.

### P4 Change the schema and verify 25 minutes

Keep a record created in P3. Add `location: Mapped[str | None]` using
`mapped_column(String(60), nullable=True)` to the model.

```bash
python -m alembic revision --autogenerate -m "add optional location"
```

Review the candidate: one added nullable location column, no dropped table or rows.
Apply it with `python -m alembic upgrade head`, then run
`python -m scripts.inspect_schema` and `python -m alembic current`.
Read the P3 row again: its id/name should remain and location should be `None`.
**Evidence:** migration file, current revision, changed schema and retained record.

### P5 Compare and explain 10 minutes

In three sentences explain when explicit SQL is helpful, when ORM is convenient,
and why either approach still needs transactions and migration discipline.
SQLite is embedded and stores this database in a local file. That file survives
an application restart but needs durable volume/storage in a deployed environment.
PostgreSQL runs as a server and supports network clients and concurrent workloads.
SQLite also has production uses; choose from requirements rather than labels.

Optional configuration demonstration only:

```bash
python -m pip install -r requirements-postgres.txt
```

A PostgreSQL URL has the form
`postgresql+psycopg://USER:PASSWORD@HOST:5432/DBNAME`.
Set it as `DATABASE_URL` only when an actual development server and credentials
exist. `.env.example` is documentation, not an automatically loaded file.
Do not put real credentials in commits. SQLite-only `check_same_thread` settings
are conditional in `database.py`. URL changes do not migrate data or prove
portability: run migrations and integration checks against PostgreSQL separately.
No PostgreSQL server is needed for the core exercise.

## CRUD API practical 65 minutes

![HTTP client calls the route, which delegates database work through a repository and request Session.](assets/request-flow.svg)

The route owns HTTP responses. The repository uses the request Session to read
or commit rows, and the database retains committed records across requests.

### C1 Guided read 10 minutes

Trace the worked POST from route to `create_equipment`, Session commit and response.
Implement `get_equipment` using the primary-key ORM pattern from P3. The GET route
already handles `None` with 404. Run the server and create then read a record in
Swagger UI. The schemas describe HTTP data; the ORM class maps a database row.

### C2 Supported listing 15 minutes

Implement `list_equipment`: build `select(Equipment).order_by(Equipment.id)` and
use `session.scalars(statement).all()`. Return a list, including `[]` when empty.
Run `python -m pytest tests/test_crud.py -k create_read -q`.

### C3 Supported replacement 15 minutes

Implement `update_equipment` and the PUT route. Look up the id, return 404 if
missing, assign **all** write fields and save/commit. The contract uses full PUT
replacement of name/category/location. An omitted location becomes null.
Keep the existing id. Repository code handles data; route code chooses HTTP status.

### C4 Partially independent core task 10 minutes

Implement DELETE end to end. Decide the lookup, database operation, transaction
boundary and route response yourself. Use the contract below. This task is required.
There is no prescribed line-by-line solution.

### C5 Integration evidence 15 minutes

Complete `test_student_write_then_read` using a different equipment example.
Assert creation, a generated id and a later GET value. The provided fixture uses
Alembic on a fresh temporary SQLite file and overrides the request Session. No test
uses your development database. Run `python -m pytest tests/test_crud.py -q`.
Also restart the development server and GET an earlier record to show file persistence.

| Contract | Success | Missing record |
|---|---|---|
| POST /equipment | 201 and object with generated id | N/A |
| GET /equipment | 200 and array | Empty array |
| GET /equipment/{id} | 200 and object | 404 |
| PUT /equipment/{id} | 200 and replaced object | 404 |
| DELETE /equipment/{id} | 204 and no body | 404 |

Example write body: `{"name":"Camera","category":"media","location":"A1"}`.
Read adds `"id": 1` (actual ids vary). Validation depth is a later lesson.

## Simple caching 40 minutes

![GET checks a dictionary. A hit returns a snapshot; a miss reads the database and stores a snapshot. A committed write invalidates its id.](assets/cache-aside.svg)

Follow the hit and miss branches. The database remains authoritative; a cached
copy is disposable. This diagram describes the required behaviour, not its code.

Spend 10 minutes tracing a miss then a hit, 20 implementing and 10 checking.
Cache only GET `/equipment/{id}`. Use the existing application dictionary, integer
ids as keys and **plain response dictionaries** as values, not Session-bound ORM objects.

1. If the key exists, return its data and set `X-Cache: hit` on `response.headers`.
2. Otherwise fetch the row, return 404 if missing, build a plain dictionary, cache
   it and set `X-Cache: miss`. Do not cache missing records in this exercise.
3. After a successful committed PUT or DELETE, remove only that id using
   `cache.pop(equipment_id, None)`. Do not invalidate before a failed transaction.
4. POST does not need per-item invalidation because a new generated id has no
   cached entry. If caching lists instead, POST would affect those lists.

Predict then verify miss, hit, PUT, miss with updated value, hit, DELETE, 404.
Run `python -m pytest tests/test_cache.py -q`, then the complete suite.
Explain why a hit need not execute a SELECT even though a request Session is supplied.

**Scope:** one local process, one dictionary, sequential lab requests, no TTL or
Redis required. Restart clears the cache but retains committed database rows.
Each worker would have a different cache. Concurrent read/write races, eviction,
bounded memory and distributed invalidation need more design before production.
TTL only limits how long an entry may survive; it does not guarantee fresh reads.
Observe hit/miss and freshness, not an invented speed-up claim.

## If you get stuck

| Symptom | Check and next action |
|---|---|
| Missing package | Confirm this terminal uses the repository's virtual environment |
| No such table/column | Run Alembic current and schema inspection against the same DATABASE_URL |
| Empty generated migration | Save model file and check models are imported in migrations/env.py |
| Data vanishes after restart | Check commit and current working directory; relative SQLite URL uses that directory |
| PendingRollbackError | Roll back the failed Session before reusing it; inspect the original exception |
| Old values after PUT | Check commit succeeds, then invalidate the integer cache key |
| 204 response has content | Return `Response(status_code=204)` after a successful delete |

Hint ladder: identify the layer that owns the failure; inspect the matching TODO
and smallest failing check; then compare the earlier worked create/read pattern.
For a missed class, first complete P1–P4, C1 and one create/read integration check.
Then complete C2–C4 and the simple cache before moving to validation work.
Stop servers with Ctrl+C. Keep your work and migration history; no cloud cleanup
is needed. Ask the lecturer for help with the exact command, error and hypothesis.
