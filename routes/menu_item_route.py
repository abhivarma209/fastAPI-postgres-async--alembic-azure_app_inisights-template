import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db_models import MenuItem
from models.menu_item import MenuItemCreate, MenuItemUpdate, MenuItemOut
from dependencies.database import get_db

router = APIRouter(prefix="/menu-items", tags=["menu items"])

@router.post("/", response_model=MenuItemOut)
async def create_menu_item(payload: MenuItemCreate, db: AsyncSession = Depends(get_db)):
    new_item = MenuItem(**payload.dict())
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item

@router.get("/", response_model=list[MenuItemOut])
async def list_menu_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MenuItem))
    return result.scalars().all()

@router.get("/{item_id}", response_model=MenuItemOut)
async def get_menu_item(item_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MenuItem).where(MenuItem.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item

@router.put("/{item_id}", response_model=MenuItemOut)
async def update_menu_item(item_id: uuid.UUID, payload: MenuItemUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MenuItem).where(MenuItem.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")

    for field, value in payload.dict().items():
        setattr(item, field, value)

    await db.commit()
    await db.refresh(item)
    return item

@router.delete("/{item_id}", response_model=dict)
async def delete_menu_item(item_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MenuItem).where(MenuItem.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")

    await db.delete(item)
    await db.commit()
    return {"message": "Menu item deleted successfully"}
