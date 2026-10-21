from alembic import context
from app.database import Base, engine
from app import models  # Register mappings before inspecting metadata.

target_metadata = Base.metadata

def offline():
    context.configure(url=engine.url.render_as_string(hide_password=False),
        target_metadata=target_metadata, literal_binds=True, compare_type=True)
    with context.begin_transaction():
        context.run_migrations()

def online():
    supplied = context.config.attributes.get('connection')
    from contextlib import nullcontext
    manager = nullcontext(supplied) if supplied is not None else engine.connect()
    with manager as connection:
        context.configure(connection=connection, target_metadata=target_metadata,
                          compare_type=True, render_as_batch=engine.dialect.name == 'sqlite')
        with context.begin_transaction():
            context.run_migrations()

offline() if context.is_offline_mode() else online()
