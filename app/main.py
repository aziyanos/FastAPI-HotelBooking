import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from app.db.database import  SessionLocal
from app.api import user, country, city
#from app.api import
#from app.admin.setup import setup_admin
import os
from fastapi.responses import HTMLResponse


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()





booking = FastAPI()

booking.include_router(user.user_router)
booking.include_router(country.country_router)
booking.include_router(city.city_router)





@booking.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head>
            <title>Booking</title>
        </head>
        <body>
            <h1>Salam Aleikum</h1>
            <p>Документация: <a href="/docs">Swagger</a></p>
        </body>
    </html>
    """




if __name__ == '__main__':
    uvicorn.run(booking, host='127.0.0.1', port=8001)