import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db_models import Restaurant
from models.restaurant import RestaurantCreate, RestaurantUpdate, RestaurantOut
from dependencies.database import get_db

router = APIRouter(prefix="/restaurants", tags=["restaurants"])

@router.post("/", response_model=RestaurantOut)
async def create_restaurant(payload: RestaurantCreate, db: AsyncSession = Depends(get_db)):
    new_restaurant = Restaurant(**payload.dict())
    db.add(new_restaurant)
    await db.commit()
    await db.refresh(new_restaurant)
    return new_restaurant

@router.get("/", response_model=list[RestaurantOut])
async def list_restaurants(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Restaurant))
    return result.scalars().all()

@router.get("/{restaurant_id}", response_model=RestaurantOut)
async def get_restaurant(restaurant_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Restaurant).where(Restaurant.id == restaurant_id))
    restaurant = result.scalar_one_or_none()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant

@router.put("/{restaurant_id}", response_model=RestaurantOut)
async def update_restaurant(restaurant_id: uuid.UUID, payload: RestaurantUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Restaurant).where(Restaurant.id == restaurant_id))
    restaurant = result.scalar_one_or_none()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    for field, value in payload.dict().items():
        setattr(restaurant, field, value)

    await db.commit()
    await db.refresh(restaurant)
    return restaurant

@router.delete("/{restaurant_id}", response_model=dict)
async def delete_restaurant(restaurant_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Restaurant).where(Restaurant.id == restaurant_id))
    restaurant = result.scalar_one_or_none()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    await db.delete(restaurant)
    await db.commit()
    return {"message": "Restaurant deleted successfully"}
