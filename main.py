from app.mqtt.mqtt_handler import run_mqtt_client
from app.mqtt.mqtt_router import router as mqtt_router 
from app.users.user_router import router as user_routers
from app.auth.router import router as auth_router

from fastapi import FastAPI

app = FastAPI()
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(mqtt_router, prefix="/mqtt", tags=["mqtt"])
app.include_router(user_routers, prefix="/user", tags=["users"])

if __name__ == "__main__":
    import uvicorn
    # TODO: add error handling for mqtt client (if it does not starts)
    run_mqtt_client()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
