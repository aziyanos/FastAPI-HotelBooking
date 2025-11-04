from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.models import Hotel
from app.db.schemas import (HotelOutSchema, HotelCreateSchema,
                        HotelUpdateSchema, HotelDetailSchema)

from app.db.database import SessionLocal

hotel_router = APIRouter(prefix="/hotel", tags=["Hotel"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@hotel_router.post("/", response_model=HotelOutSchema)
async def create_hotel(hotel_data: HotelCreateSchema, db: Session = Depends(get_db)):
    new_hotel = Hotel(**hotel_data.dict())

    db.add(new_hotel)
    db.commit()
    db.refresh(new_hotel)
    return new_hotel


@hotel_router.get("/", response_model=List[HotelOutSchema])
async def list_hotel(db: Session = Depends(get_db)):
    return db.query(Hotel).all()



@hotel_router.get("/{hotel_id}/", response_model=HotelDetailSchema)
async def detail_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel_db = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel_db:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return hotel_db


@hotel_router.put("/{hotel_id}/", response_model=HotelOutSchema)
async def update_hotel(hotel_data: HotelUpdateSchema, hotel_id: int, db: Session = Depends(get_db)):
    hotel_db = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel_db:
        raise HTTPException(status_code=404, detail="Hotel not found")
    hotel_db.hotel_name = hotel_data.hotel_name
    hotel_db.stars = hotel_data.stars
    hotel_db.street = hotel_data.street
    hotel_db.postal_index = hotel_data.postal_index
    hotel_db.description = hotel_data.description
    hotel_db.country_id = hotel_data.country_id
    hotel_db.city_id = hotel_data.city_id
    hotel_db.owner_id = hotel_data.owner_id
    db.commit()
    db.refresh(hotel_db)
    return hotel_db


@hotel_router.delete("/{hotel_id}/")
async def delete_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel_db = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel_db:
        raise HTTPException(status_code=404, detail="Hotel not found")
    db.delete(hotel_db)
    db.commit()
    return {"message": f"Hotel {hotel_id} deleted successfully"}
