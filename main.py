from fastapi import FastAPI
from apifunctions import getACS, getElta, getSpeedex
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="eltrak",
              description="""**eltrak** intends to become a free to use API to get shipping status for Greek courier services.
              <br>Currently, it **only** supports **ACS, Elta Courier and Speedex Courier**. Due to lack of tracking numbers in a variety of states
              to test with, some errors are to be expected.
              <br>Geniki Tachidromiki will follow soon. Any help is welcome. Even if you just provide me with test tracking numbers.""",
              version="1.0.3", docs_url="/documentation", redoc_url=None
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
def trackACS(tracking):
    """Tracks ACS vouchers 

    Parameters:
    tracking (str): Tracking number
   """
    response = getACS(tracking=tracking)
    return response


@ app.get("/v1/track/elta/{tracking}")
def trackElta(tracking):
    """Tracks Elta Courier vouchers 

    Parameters:
    tracking (str): Tracking number
   """
    response = getElta(tracking=tracking)
    return response
