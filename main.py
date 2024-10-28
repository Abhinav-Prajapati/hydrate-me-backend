from app.database.db import get_db_session
from app.database.models import Users 
from app.mqtt.mqtt_handler import run_mqtt_client
from app.mqtt.mqtt_router import router as mqtt_router 

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel, EmailStr

from app.auth.router import router as auth_router

app = FastAPI()
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(mqtt_router, prefix="/mqtt", tags=["mqtt"])


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password_hash: str  # Assume password is already hashed before storing
    sensor_id: Optional[str] = None
    currect_water_level_in_bottle: Optional[int] = None
    bottle_weight: Optional[int] = None
    is_bottle_on_dock: Optional[bool] = None
    daily_goal: Optional[int] = None
    wakeup_time: Optional[str] = None
    sleep_time: Optional[str] = None
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    gender: Optional[str] = None
    
class UserRead(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True  # Allows using ORM objects directly with Pydantic

# API route to create a new user
@app.post("/users/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db_session)):
    db_user = Users(
        username=user.username,
        email=user.email,
        password_hash=user.password_hash,
        sensor_id=user.sensor_id,
        currect_water_level_in_bottle=user.currect_water_level_in_bottle,
        bottle_weight=user.bottle_weight,
        is_bottle_on_dock=user.is_bottle_on_dock,
        daily_goal=user.daily_goal,
        wakeup_time=user.wakeup_time,
        sleep_time=user.sleep_time,
        age=user.age,
        weight=user.weight,
        height=user.height,
        gender=user.gender
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# API route to retrieve a user by ID
@app.get("/users/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db_session)):
    db_user = db.query(Users).filter(Users.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Main function to run the application
if __name__ == "__main__":
    import uvicorn
    
    # TODO: add error handling for mqtt client
    run_mqtt_client()
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
