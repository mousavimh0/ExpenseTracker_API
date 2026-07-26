from fastapi import FastAPI
from routers.transactions import transaction_router
from routers.report import report_router

app = FastAPI()

app.include_router(router= transaction_router ,prefix= "/transactions")
app.include_router(router= report_router, prefix="/report")
