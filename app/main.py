
from fastapi import FastAPI
from app.database.connection import Base, engine
from app.routes.user_routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="device_systems API",
    description="Proyecto EV09 ADSO",
    version="1.0"
)

app.include_router(router)

@app.get('/')
def home():
    return {'mensaje':'API funcionando'}
