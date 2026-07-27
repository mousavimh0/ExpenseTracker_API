from fastapi import FastAPI
from app.routers.transactions import transaction_router
from app.routers.report import report_router
from app.database import engine, Base
from app.models import db_models

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(router= transaction_router ,prefix= "/transactions")
app.include_router(router= report_router, prefix="/report")
