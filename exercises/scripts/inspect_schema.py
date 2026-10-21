from sqlalchemy import inspect
from app.database import engine
print([(c['name'], c['nullable']) for c in inspect(engine).get_columns('equipment')])
