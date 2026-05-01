# main.py

from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="Sports Match Intelligence Agent")

app.include_router(router)
