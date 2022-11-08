from pydantic import BaseModel


class FirstAddress(BaseModel):
    name: str
    street: str 
    address: str | None = None
    latitude: str | None = None
    longitude: str | None = None
    city: str | None = None

class FinalAddress(FirstAddress):
    id: int

    class Config:
        orm_mode = True