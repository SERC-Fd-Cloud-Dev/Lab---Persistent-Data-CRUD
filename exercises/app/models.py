from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Equipment(Base):
    __tablename__ = 'equipment'
    id: Mapped[int] = mapped_column(primary_key=True)
    # TODO P1: map name (String(80)) and category (String(40)), both required.
    # TODO P4: after saving data, add nullable location (String(60)) and migrate.
