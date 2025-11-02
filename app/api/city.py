from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import City
from app.db.schemas import CityCreate, CityOut
from typing import List


city_router = APIRouter(prefix="/cities", tags=["Cities"])


@city_router.post('/', response_model=CityOut)
async def create_city(city: CityCreate, db: Session = Depends(get_db)):
    new_city = City(city_name=city.city_name, city_image=city.city_image)

    db.add(new_city)
    db.commit()
    db.refresh(new_city)
    return new_city


@city_router.get('/', response_model=List[CityOut])
async def list_cities(db: Session = Depends(get_db)):
    return db.query(City).all()


@city_router.get('/{city_id}/', response_model=CityOut)
async def detail_city(city_id: int, db: Session = Depends(get_db)):
    city = db.query(City).filter(City.id == city_id).first()

    if not city:
        raise HTTPException(status_code=404, detail='City not found')
    return city


@city_router.put('/{city_id}/', response_model=CityOut)
async def update_city(city_id: int, city_data: CityCreate, db: Session = Depends(get_db)):
    city = db.query(City).filter(City.id == city_id).first()

    if not city:
        raise HTTPException(status_code=404, detail='City not found')

    city.city_name = city_data.city_name
    city.city_image = city_data.city_image

    db.commit()
    db.refresh(city)
    return city


@city_router.delete('/{city_id}/')
async def delete_city(city_id: int, db: Session = Depends(get_db)):
    city = db.query(City).filter(City.id == city_id).first()

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    db.delete(city)
    db.commit()
    return {'message': f'City {city_id} deleted successfully'}