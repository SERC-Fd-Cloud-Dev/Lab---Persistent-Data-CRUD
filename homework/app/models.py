from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Guess(Base):
    __tablename__ = 'guesses'
    id: Mapped[int] = mapped_column(primary_key=True)
    # TODO: map player String(40), clue_id int, title String(120), correct bool.
