import uuid

from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Text, Boolean, DateTime, func
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

class Customer(Base):
    __tablename__ = "customer"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String, nullable=False)

class InventoryStatusMapping(Base):
    __tablename__ = "inventory_status_mapping"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_system = Column(
        String(50), nullable=False
    )  # "sap" | "logiwa" | "spyglass" | "salesforce"
    column_mappings = Column(JSON, nullable=False)  # List of ColumnMapping objects
    result_status = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())