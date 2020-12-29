from fastapi import FastAPI
from apifunctions import getACS, getSpeedex
from fastapi.middleware.cors import CORSMiddleware
from eltrac import speedex

app = FastAPI(title="eltrak",
              description="**eltrak** intends to become a free to use API to get shipping status for Greek courier services.<br>Currently, it **only** supports **Speedex and ACS Courier**. ACS functionality is not tested properly and may return No data due to unknown errors. <br>Next step will be Elta Courier and soon Geniki Tachidromiki will follow. Any help is welcome.",
              version="0.0.2", docs_url="/documentation", redoc_url=None
              )
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@ app.get("/")
def general():
    return {"Project": "eltrak", "Repository": "https://github.com/gntouts/eltrak", "Documentation": "https://eltrak.herokuapp.com/documentation"}


@ app.get("/v1/track/speedex/{tracking}")
def trackSpeedex(tracking):
    """Tracks Speedex vouchers 

    Parameters:
    tracking (str): Tracking number
   """
    response = getSpeedex(tracking=tracking)
    return response


@ app.get("/v1/track/acs/{tracking}")
def trackSpeedex(tracking):
    """Tracks ACS vouchers 

    Parameters:
    tracking (str): Tracking number
   """
    response = getACS(tracking=tracking)
    return response
