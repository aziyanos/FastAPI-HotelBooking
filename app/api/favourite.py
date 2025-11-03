from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.models import Favourite
from app.db.schemas import FavouriteSchema
from app.db.database import SessionLocal

favourite_router = APIRouter(prefix="/favourite", tags=["Favourite"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@favourite_router.post("/", response_model=FavouriteSchema)
async def create_favourite(favourite_data: FavouriteSchema, db: Session = Depends(get_db)):
    new_favourite = Favourite(user_id=favourite_data.user_id)
    db.add(new_favourite)
    db.commit()
    db.refresh(new_favourite)
    return new_favourite


@favourite_router.get("/", response_model=List[FavouriteSchema])
async def list_favourites(db: Session = Depends(get_db)):
    return db.query(Favourite).all()


@favourite_router.get("/{favourite_id}/", response_model=FavouriteSchema)
async def detail_favourite(favourite_id: int, db: Session = Depends(get_db)):
    favourite_db = db.query(Favourite).filter(Favourite.id == favourite_id).first()
    if not favourite_db:
        raise HTTPException(status_code=404, detail="Favourite not found")
    return favourite_db



@favourite_router.put("/{favourite_id}/", response_model=FavouriteSchema)
async def update_favourite(favourite_data: FavouriteSchema, favourite_id: int, db: Session = Depends(get_db)):
    favourite_db = db.query(Favourite).filter(Favourite.id == favourite_id).first()
    if not favourite_db:
        raise HTTPException(status_code=404, detail="Favourite not found")

    favourite_db.user_id = favourite_data.user_id
    db.commit()
    db.refresh(favourite_db)
    return favourite_db



@favourite_router.delete("/{favourite_id}/")
async def delete_favourite(favourite_id: int, db: Session = Depends(get_db)):
    favourite_db = db.query(Favourite).filter(Favourite.id == favourite_id).first()
    if not favourite_db:
        raise HTTPException(status_code=404, detail="Favourite not found")
    db.delete(favourite_db)
    db.commit()
    return {"message": f"Favourite {favourite_id} deleted successfully"}

