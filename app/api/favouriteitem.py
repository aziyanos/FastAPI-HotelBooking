from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.models import FavouriteItem
from app.db.schemas import FavouriteItemSchema
from app.db.database import SessionLocal

favouriteitem_router = APIRouter(prefix="/favouriteitem", tags=["FavouriteItem"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@favouriteitem_router.post("/", response_model=FavouriteItemSchema)
async def create_favourite_item(favourite_item_data: FavouriteItemSchema, db: Session = Depends(get_db)):
    new_favourite_item = FavouriteItem(
        favourite_id=favourite_item_data.favourite_id,
        hotel_id=favourite_item_data.hotel_id
    )
    db.add(new_favourite_item)
    db.commit()
    db.refresh(new_favourite_item)
    return new_favourite_item



@favouriteitem_router.get("/", response_model=List[FavouriteItemSchema])
async def list_favourite_item(db: Session = Depends(get_db)):
    return db.query(FavouriteItem).all()



@favouriteitem_router.get("/{favouriteitem_id}/", response_model=FavouriteItemSchema)
async def detail_favourite_item(favouriteitem_id: int, db: Session = Depends(get_db)):
    favourite_item_db = db.query(FavouriteItem).filter(FavouriteItem.id == favouriteitem_id).first()
    if not favourite_item_db:
        raise HTTPException(status_code=404, detail="Favourite item not found")
    return favourite_item_db



@favouriteitem_router.put("/{favouriteitem_id}/", response_model=FavouriteItemSchema)
async def update_favourite_item(favourite_item_data: FavouriteItemSchema, favouriteitem_id: int,
                                db: Session = Depends(get_db)):
    favourite_item_db = db.query(FavouriteItem).filter(FavouriteItem.id == favouriteitem_id).first()
    if not favourite_item_db:
        raise HTTPException(status_code=404, detail="Favourite item not found")

    favourite_item_db.favourite_id = favourite_item_data.favourite_id
    favourite_item_db.hotel_id = favourite_item_data.hotel_id
    db.commit()
    db.refresh(favourite_item_db)
    return favourite_item_db



@favouriteitem_router.delete("/{favouriteitem_id}/")
async def delete_favourite_item(favouriteitem_id: int, db: Session = Depends(get_db)):
    favourite_item_db = db.query(FavouriteItem).filter(FavouriteItem.id == favouriteitem_id).first()
    if not favourite_item_db:
        raise HTTPException(status_code=404, detail="Favourite item not found")
    db.delete(favourite_item_db)
    db.commit()
    return {"message": f"Favourite item {favouriteitem_id} deleted successfully"}
