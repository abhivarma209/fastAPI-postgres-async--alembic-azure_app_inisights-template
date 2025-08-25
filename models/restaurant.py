import uuid
from pydantic import BaseModel

class RestaurantBase(BaseModel):
    name: str
    street_address: str
    description: str | None = None

class RestaurantCreate(RestaurantBase):
    pass

class RestaurantUpdate(RestaurantBase):
    pass

class RestaurantOut(RestaurantBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
