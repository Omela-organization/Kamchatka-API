import json
import os
import asyncio
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.db.base_model import init_models, dispose_engine, drop_models
from src.routers.base_router import base_router

os.makedirs("photos", exist_ok=True)
os.makedirs("documents", exist_ok=True)

app = FastAPI(
    description="API для ECO_Kamchatka",
    title="API для ECO_Kamchatka",
    version="0.1.0",
    debug=False
)


@app.on_event("startup")
async def startup():
    # await drop_models()
    await init_models()
    openapi_data = app.openapi()
    # Change "openapi.json" to desired filename
    with open("openapi.json", "w") as file:
        json.dump(openapi_data, file)


@app.on_event("shutdown")
async def shutdown():
    await dispose_engine()


origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(base_router)
