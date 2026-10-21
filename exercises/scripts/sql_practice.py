"""Run after the first migration. No location column is needed yet."""
from sqlalchemy import text
from app.database import SessionLocal

with SessionLocal() as session:
    # Guided INSERT. Bound values remain data rather than SQL syntax.
    session.execute(text('INSERT INTO equipment (name, category) VALUES (:name, :category)'),
                    {'name': 'SQL microscope', 'category': 'optics'})
    session.commit()
    rows = session.execute(text('SELECT id, name FROM equipment WHERE name = :name'),
                           {'name': 'SQL microscope'}).mappings().all()
    print([dict(row) for row in rows])
    # TODO P2: UPDATE only this practice record by its id, then commit.
    # TODO P2: SELECT again to verify the update, DELETE it by id, then commit.
    # Keep an ORM-created record for the later migration data-preservation check.
