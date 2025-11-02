from fastapi import HTTPException, Depends, APIRouter
from app.db.models import Country
from app.db.schemas import CountryOutSchema, CountryUpdateSchema, CountryCreateSchema
from app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



country_router = APIRouter(prefix='/country', tags=['Country'])


@country_router.post('/', response_model=CountryOutSchema)
async def create_country(country_data: CountryCreateSchema, db: Session = Depends(get_db)):

    new_country = Country(country_name=country_data.country_name,
                          country_image=country_data.country_image)

    db.add(new_country)
    db.commit()
    db.refresh(new_country)
    return new_country



@country_router.get('/', response_model=List[CountryOutSchema])
async def list_country(db: Session = Depends(get_db)):
    return db.query(Country).all()


@country_router.get('/{country_id}/', response_model=CountryOutSchema)
async def detail_country(country_id: int, db: Session = Depends(get_db)):
    country_db = db.query(Country).filter(Country.id == country_id).first()

    if country_db is None:
        raise HTTPException(status_code=404, detail='Country not found')
    return country_db



@country_router.put('/{country_id}/', response_model=CountryOutSchema)
async def update_country(country_data: CountryUpdateSchema, country_id: int,
                         db: Session = Depends(get_db)):
    country_db = db.query(Country).filter(Country.id == country_id).first()

    if country_db is None:
        raise HTTPException(status_code=404, detail='Country not updated')

    country_db.country_name =  country_data.country_name
    country_db.country_image = country_data.country_image

    db.commit()
    db.refresh(country_db)

    return country_db



@country_router.delete('/{country_id}/')
async def delete_country(country_id: int, db: Session = Depends(get_db)):
    country_db = db.query(Country).filter(Country.id == country_id).first()

    if country_db is None:
        raise HTTPException(status_code=404, detail='User not found')

    db.delete(country_db)
    db.commit()
    return {'message': f'Country {country_id} deleted successfully'}




