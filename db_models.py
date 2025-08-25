import uuid

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from dependencies.database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String, nullable=False)
    street_address = Column(String, nullable=False)
    description = Column(String)

class MenuItem(Base):
    __tablename__ = "menu_items"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey("restaurants.id"), nullable=False)
    name = Column(String, nullable=False)
    price = Column(Integer)
