import uuid
from pydantic import BaseModel

class MenuItemBase(BaseModel):
    name: str
    price: int
    restaurant_id: uuid.UUID

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemUpdate(MenuItemBase):
    pass

class MenuItemOut(MenuItemBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
