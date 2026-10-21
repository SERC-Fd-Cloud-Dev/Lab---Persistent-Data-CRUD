# Exercise 3: Local dictionary caching

Add a small cache-aside path for GET `/equipment/{id}`. A cache is a faster,
temporary place to keep data that an application may need again. In this lab the
cache is one Python dictionary in the API process. The database remains the
authoritative, persistent store; cached data is only a disposable copy.

Complete Exercises 1 and 2 first so the routes and database operations already
work. This exercise starts with guided observation, moves to supported
implementation, and finishes with partially independent verification and
explanation.

Work from the `exercises/` directory and use the setup from
[Exercise 1](exercise-1.md). Your implementation belongs in `app/main.py`; the
supplied `tests/test_cache.py` checks behavior. Keep its assertions unchanged.

## Guided start: observe the cache-aside flow

![GET checks a dictionary. A hit returns a snapshot; a miss reads the database and stores a snapshot. A committed write invalidates its id.](assets/cache-aside.svg)

The route first checks the dictionary. A **hit** means the requested id is
already cached, so the route can return that saved response without reading the
database. A **miss** means it is not cached: the route reads the row from the
database, turns it into response data and saves a copy in the dictionary for
next time. The database remains the source of truth on a miss.

Trace both branches in the diagram. Then predict what should happen when you GET
the same id twice, update it with PUT, GET it again and DELETE it. On the first
GET expect a miss; on the second expect a hit. After a successful update, the
next GET should miss and return the new value. After deletion, GET should return
404 rather than the old cached copy.

## Supported practice: implement the required behavior

Cache only GET `/equipment/{id}`. Use the existing application dictionary,
integer ids as keys and **plain response dictionaries** as values. A plain
dictionary is a snapshot of the response fields at the time of the read. Do not
cache a SQLAlchemy ORM object: it belongs to a Session, which closes after the
request, and is not the response data contract.

1. Look for the integer id in the dictionary. If present, return its snapshot and
   set `X-Cache: hit` on `response.headers`.
2. If absent, fetch the row from the repository. Return 404 if it does not exist;
   do not cache missing records in this exercise. For an existing row, build a
   plain response dictionary, cache it under its id and set `X-Cache: miss`.
3. After a PUT has successfully committed, remove only that id from the
   dictionary with `cache.pop(equipment_id, None)`. DELETE must do the same after
   a successful commit. Invalidation means removing the saved copy so the next
   read must fetch current database data. Do not invalidate before a transaction
   succeeds: a failed write should not discard a still-valid snapshot.
4. POST does not need per-item invalidation because a new generated id has no
   cached entry. If you chose to cache the equipment list instead, POST would
   also require invalidating that list.

Check your work as you implement each step. The response header lets a client
observe whether the route used the cache; it does not claim that the request is
faster.

```bash
python -m pytest tests/test_cache.py -q
```

## Partially independent finish: verify and explain

Now verify the full sequence without following a line-by-line recipe. Use a
created equipment record and the HTTP contract from Exercise 2. Confirm that a
GET miss is followed by a hit; after a successful PUT, the next GET is a miss
with the updated value; another GET is a hit; and after DELETE, GET returns 404.
Check both response data and `X-Cache` headers.

Run the cache check, then the full suite:

```bash
python -m pytest tests/test_cache.py -q
python -m pytest -q
```

In your own words, explain why a cache hit need not execute a SELECT even though
a request Session is supplied, why cached values should be plain snapshots, and
why invalidation must happen only after a successful write. If a check fails,
identify which step of the request flow is responsible before changing code.

## Scope and troubleshooting

This activity intentionally uses one process-local dictionary and sequential lab
requests. There is no TTL (time-to-live, or automatic expiry after a duration) or
Redis (a separate data-store service) in this exercise. Restarting the API clears
the dictionary but leaves committed database rows in the SQLite file. Each
application worker would have its own dictionary, so one worker's invalidation
would not update another worker's cached copy.

Concurrent reads and writes can create races; a production cache also needs
decisions about eviction, bounded memory and consistency across workers. A TTL
only limits how long an entry may remain; it does not guarantee fresh reads in
every situation. For this exercise, observe the hit/miss behavior and whether
updates are reflected correctly. Do not claim a speed improvement without
measuring it.

| Symptom | Check and next action |
|---|---|
| Old values after PUT | Check the commit succeeds, then invalidate the integer cache key |
| Deleted row remains readable | Confirm successful DELETE invalidates the id and a later GET returns 404 |
| Cache test fails | Check plain dictionary snapshots, integer keys and `X-Cache` values |

## Minimum catch-up and teardown

If you missed a class, first complete Exercise 1 P1–P4, then Exercise 2's guided
read and one create/read check. Next complete Exercise 2's listing, replacement
and DELETE core tasks, then return here for the cache behavior. Ask the lecturer
for help with the exact command, error and hypothesis.

Stop servers with Ctrl+C. Keep your work and migration history. No cloud cleanup
is needed.
