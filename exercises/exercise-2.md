# Exercise 2: CRUD API

Build on Exercise 1 to finish the equipment API's reads, replacement and deletion.
The guided start and supported practice lead to a partially independent core
finish: you will design DELETE end to end and add a write/read integration check.

Work from the `exercises/` directory and use the environment and database setup
from [Exercise 1](exercise-1.md). Stop the development server before changing
schema or migration files.

Your implementation files are `app/repository.py`, `app/main.py` and
`tests/test_crud.py`. Keep the existing route signatures and assertions.

## CRUD API practical — 65 minutes

![HTTP client calls the route, which delegates database work through a repository and request Session.](assets/request-flow.svg)

The route owns HTTP responses. The repository uses the request Session to read or
commit rows, and the database retains committed records across requests.

### C1: Guided read — 10 minutes

Trace the worked POST from route to `create_equipment`, Session commit and
response. Implement `get_equipment` using the primary-key ORM pattern from
Exercise 1. The GET route already handles `None` with 404. Run the server and
create then read a record in Swagger UI. The schemas describe HTTP data; the ORM
class maps a database row.

### C2: Supported listing — 15 minutes

Implement `list_equipment`: build
`select(Equipment).order_by(Equipment.id)` and use
`session.scalars(statement).all()`. Return a list, including `[]` when empty.

```bash
python -m pytest tests/test_crud.py -k create_read -q
```

### C3: Supported replacement — 15 minutes

Implement `update_equipment` and the PUT route. Look up the id, return 404 if
missing, assign **all** write fields and save/commit. The contract uses full PUT
replacement of name/category/location. An omitted location becomes null. Keep the
existing id. Repository code handles data; route code chooses HTTP status.

**Checkpoint:** Create an item in Swagger UI, then send a PUT to its
`/equipment/{id}` path with a changed name and all write fields. Confirm the
response is 200 with the same id and replaced values. GET the item again and
confirm the new values persisted. Try a nonexistent id and check for 404. You can
also run the supplied replacement check:
`python -m pytest tests/test_crud.py -k test_replace_and_delete -q`. This test
checks the replacement and its subsequent read before it checks deletion.

| Contract | Success | Missing record |
|---|---|---|
| POST /equipment | 201 and object with generated id | N/A |
| GET /equipment | 200 and array | Empty array |
| GET /equipment/{id} | 200 and object | 404 |
| PUT /equipment/{id} | 200 and replaced object | 404 |
| DELETE /equipment/{id} | 204 and no body | 404 |

Example write body: `{"name":"Camera","category":"media","location":"A1"}`.
Read adds `"id": 1` (actual ids vary). Validation depth is a later lesson.

## Hints and troubleshooting

| Symptom | Check and next action |
|---|---|
| PUT returns old values | Check that the replacement assigns all fields and commits |
| 204 response has content | Return `Response(status_code=204)` after a successful delete |
| CRUD checks fail before their milestone | Complete the matching TODO; the scaffold intentionally leaves core operations unfinished |

Identify whether a failure is in the HTTP contract, query, transaction or schema.
Inspect the smallest failing test and compare it with the worked POST path. Keep
the existing assertions and use the temporary test database supplied by the
fixture.

Continue to [Exercise 3](exercise-3.md) for cache-aside reads and invalidation.

## Partially independent core finish

The guided start and supported practice are complete. Finish by applying the
patterns yourself: make the design decisions, then use the contract and tests to
check your work. These are required core tasks; the scaffold intentionally leaves
them unfinished.

### C4: DELETE end to end — 10 minutes

Implement DELETE. Decide how to look up the equipment, perform the database
operation, set the transaction boundary and choose the route response. A
successful deletion returns 204 with no response body; an unknown id returns
404. Keep the existing route signature and contract assertions.

### C5: Write/read integration evidence — 15 minutes

Complete `test_student_write_then_read` in `tests/test_crud.py` using a different
equipment example. Check that creation succeeds, the response has a generated
id, and a later GET returns the value you wrote. The supplied fixture applies
Alembic to a fresh temporary SQLite file and overrides the request Session; it
does not use your development database.

```bash
python -m pytest tests/test_crud.py -q
```

Then restart the development server and GET an earlier record to confirm that a
committed record remains in the SQLite file.
