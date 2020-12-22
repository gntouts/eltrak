from fastapi import FastAPI
from apifunctions import getSpeedex
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Project": "eltrak", "Repository": "https://github.com/gntouts/eltrak"}


@app.get("/v1/track/speedex/{tracking}")
def trackSpeedex(tracking: int):
    response = getSpeedex(tracking=tracking)
    return response
