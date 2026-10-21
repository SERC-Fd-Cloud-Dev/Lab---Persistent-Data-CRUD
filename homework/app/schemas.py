from pydantic import BaseModel, ConfigDict

class GuessWrite(BaseModel):
    player: str
    clue_id: int
    title: str

class GuessRead(GuessWrite):
    model_config = ConfigDict(from_attributes=True)
    id: int
    correct: bool
