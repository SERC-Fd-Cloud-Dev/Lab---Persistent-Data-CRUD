from pydantic import BaseModel, ConfigDict

class EquipmentWrite(BaseModel):
    name: str
    category: str
    location: str | None = None

class EquipmentRead(EquipmentWrite):
    model_config = ConfigDict(from_attributes=True)
    id: int
