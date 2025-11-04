from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, List
from app.db.models import RoomStatus, BookingStatus, RoomType, RoleChoices
from datetime import datetime, date



class CountryOutSchema(BaseModel):
    id: int
    country_name: str
    country_image: str

    class Config:
        from_attributes = True


class CountryCreateSchema(BaseModel):
    country_name: str
    country_image: str

    class Config:
        from_attributes = True


class CountryUpdateSchema(BaseModel):
    country_name: str
    country_image: str

    class Config:
        from_attributes = True


class UserProfileSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    user_name: str
    email: EmailStr
    age: Optional[int] = None
    phone_number: Optional[str] = None
    role: RoleChoices
    created_date: datetime


    class Config:
        from_attributes = True


class UserProfileLoginSchema(BaseModel):
    user_name: EmailStr
    password: str


class UserProfileCreateSchema(BaseModel):
    first_name: str
    last_name: str
    user_name: str
    age: Optional[int] = Field(None, ge=0, le=150)
    email: EmailStr
    user_name: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)


class UserProfileUpdateSchema(BaseModel):
    first_name: Optional[str] = Field(None, min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    user_name: Optional[str] = Field(None, min_length=3, max_length=50)
    age: Optional[int] = Field(None, ge=0, le=150)
    phone_number: Optional[str] = None


class ChangePasswordSchema(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=8)


class CityBase(BaseModel):
    city_name: str
    city_image: Optional[str] = None

class CityCreate(CityBase):
    pass

class CityOut(CityBase):
    id: int

    class Config:
        from_attributes = True


class ServiceSchema(BaseModel):
    id: int
    service_name: str
    service_image: str

    class Config:
        from_attributes = True


class HotelOutSchema(BaseModel):
    id: int
    hotel_name: str
    stars: Optional[int] = Field(None, gt=0, lt=6)
    postal_index: str
    description: str
    street: str
    country_id: int
    city_id: int
    owner_id: int

    class Config:
        from_attributes = True


class HotelDetailSchema(BaseModel):
    id: int
    hotel_name: str
    stars: Optional[int] = Field(None, ge=1, le=5)
    postal_index: str
    description: str
    street: str
    country_id: int
    city_id: int
    owner_id: int

    class Config:
        from_attributes = True


class HotelCreateSchema(BaseModel):
    hotel_name: str = Field(..., min_length=2, max_length=200)
    stars: Optional[int] = Field(None, ge=1, le=5)  # от 1 до 5 звёзд
    postal_index: str = Field(..., min_length=4, max_length=20)
    description: str = Field(..., min_length=10, max_length=2000)
    street: str = Field(..., min_length=3, max_length=200)
    country_id: int = Field(..., gt=0)
    city_id: int = Field(..., gt=0)


class HotelUpdateSchema(BaseModel):
    hotel_name: Optional[str] = Field(None, min_length=2, max_length=200)
    stars: Optional[int] = Field(None, ge=1, le=5)
    postal_index: Optional[str] = Field(None, min_length=4, max_length=20)
    description: Optional[str] = Field(None, min_length=10, max_length=2000)
    street: Optional[str] = Field(None, min_length=3, max_length=200)
    country_id: Optional[int] = Field(None, gt=0)
    city_id: Optional[int] = Field(None, gt=0)


class HotelImageSchema(BaseModel):
    id: int
    hotel_image: str

    class Config:
        from_attributes = True


class RoomSchema(BaseModel):
    id: int
    room_number: str
    room_type: RoomType
    room_status: RoomStatus
    room_description: str
    price: float
    max_guests: int

    class Config:
        from_attributes = True


class RoomImageSchema(BaseModel):
    id:int
    room_image: str

    class Config:
        from_attributes = True


class BookingSchema(BaseModel):
    id:int
    check_in: date
    check_out: date
    booking_status: BookingStatus
    hotel_id: int
    room_id: int
    user_id: int

    class Config:
        from_attributes = True


class ReviewSchema(BaseModel):
    id: int
    stars: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None

    class Config:
        from_attributes = True


class FavouriteSchema(BaseModel):
    id: int
    user_id: int


    class Config:
        from_attributes = True


class FavouriteItemSchema(BaseModel):
    id: int
    favourite_id: int
    hotel_id: int

    class Config:
        from_attributes = True