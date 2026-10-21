from sqlalchemy import select
from app.models import Equipment

def save(session, item):
    try:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item
    except Exception:
        session.rollback()
        raise

def create_equipment(session, data):
    # Worked create pattern. This needs the completed model and migrations.
    return save(session, Equipment(**data))

def get_equipment(session, equipment_id):
    raise NotImplementedError('C1: fetch Equipment by primary key')

def list_equipment(session):
    raise NotImplementedError('C2: return a list ordered by id')

def update_equipment(session, equipment_id, data):
    raise NotImplementedError('C3: return None if missing, otherwise replace fields and save')

def delete_equipment(session, equipment_id):
    raise NotImplementedError('C4: return False if missing, otherwise delete and commit')
