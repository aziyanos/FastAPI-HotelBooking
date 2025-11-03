from fastapi import HTTPException, Depends, APIRouter
from app.db.models import Service
from app.db.schemas import ServiceSchema
from app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


service_router = APIRouter(prefix='/service', tags=['Service'])



@service_router.post('/', response_model=ServiceSchema)
async def create_service(service_data: ServiceSchema, db: Session = Depends(get_db)):
    new_service = Service(
        service_name=service_data.service_name,
        service_image=service_data.service_image
    )

    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return new_service


@service_router.get('/', response_model=List[ServiceSchema])
async def list_services(db: Session = Depends(get_db)):
    return db.query(Service).all()


@service_router.get('/{service_id}/', response_model=ServiceSchema)
async def detail_service(service_id: int, db: Session = Depends(get_db)):
    service_db = db.query(Service).filter(Service.id == service_id).first()

    if service_db is None:
        raise HTTPException(status_code=404, detail='Service not found')
    return service_db


@service_router.put('/{service_id}/', response_model=ServiceSchema)
async def update_service(service_data: ServiceSchema, service_id: int, db: Session = Depends(get_db)):
    service_db = db.query(Service).filter(Service.id == service_id).first()

    if service_db is None:
        raise HTTPException(status_code=404, detail='Service not found')

    service_db.service_name = service_data.service_name
    service_db.service_image = service_data.service_image

    db.commit()
    db.refresh(service_db)
    return service_db


@service_router.delete('/{service_id}/')
async def delete_service(service_id: int, db: Session = Depends(get_db)):
    service_db = db.query(Service).filter(Service.id == service_id).first()

    if service_db is None:
        raise HTTPException(status_code=404, detail='Service not found')

    db.delete(service_db)
    db.commit()
    return {'message': f'Service {service_id} deleted successfully'}

