from app.database import SessionLocal
from app.models import Equipment

with SessionLocal() as session:
    item = Equipment(name='ORM microscope', category='optics')
    session.add(item)
    session.commit()
    session.refresh(item)
    print(item.id, item.name)
    # TODO P3: retrieve the same record with session.get(Equipment, item.id).
    # Change its name, commit and print its new value. Keep this row for P4.
