from fastapi import FastAPI
from app.api.manual_input_api import router as manual_router
from app.api.extract import router as extract_router

app = FastAPI(title="Email Invoice Automation")

app.include_router(manual_router)
app.include_router(extract_router)
