from EltrakLib.TrackerFactory import get_factory, CourierNotSupportedError
from EltrakLib.BaseClasses import InvalidTrackingNumber
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from apifunctions import getACS, getElta, getSpeedex, getGeniki
from enum import Enum

app = FastAPI(title="eltrak",
              description="""**eltrak** intends to become a free to use API to get shipping status for Greek courier services.
              <br>Currently, it **only** supports **ACS, Elta Courier and Speedex Courier**. Due to lack of tracking numbers in a variety of states
              to test with, some errors are to be expected.
              <br> Any help is welcome. Even if you just provide me with test tracking numbers.""",
              version="1.0.4", docs_url="/documentation", redoc_url="/redoc"
              )
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class CourierName(str, Enum):
    speedex = "speedex"
    acs = "acs"
    elta = "elta"


@ app.get("/")
def general():
    return {"Project": "eltrak", "Repository": "https://github.com/gntouts/eltrak", "Documentation": "https://eltrak.herokuapp.com/documentation"}


@app.get('/v2/track/{courier}/{tracking_number}')
def track_courier(courier: CourierName, tracking_number: str):
    try:
        courier = str(courier).split('.')[-1]
        factory = get_factory(courier)
        tracker = factory.get_tracker()
        result = tracker.track(tracking_number)
        return result
    except InvalidTrackingNumber as e:
        raise HTTPException(
            status_code=404,
            detail=e.message,
            headers={"X-Error": "InvalidTrackingNumber"},
        )
    except CourierNotSupportedError as e:
        raise HTTPException(
            status_code=404,
            detail=e.message,
            headers={"X-Error": "CourierNotSupportedError"},
        )
    except:
        raise HTTPException(
            status_code=500,
            detail='Unknow error. Please provide more details for debugging.',
            headers={"X-Error": "UnkownError"},
        )


@ app.get("/v1/track/speedex/{tracking}", tags=["v1"], deprecated=True)
def trackSpeedex(tracking):
    """Tracks Speedex vouchers 

    Parameters:
    tracking (str): Tracking number
   """
    response = getSpeedex(tracking=tracking)
    return response


@ app.get("/v1/track/acs/{tracking}", tags=["v1"], deprecated=True)
def trackACS(tracking):
    """Tracks ACS vouchers 

    Parameters:
    tracking (str): Tracking number
   """
    response = getACS(tracking=tracking)
    return response


@ app.get("/v1/track/elta/{tracking}", tags=["v1"], deprecated=True)
def trackElta(tracking):
    """Tracks Elta Courier vouchers 

    Parameters:
    tracking (str): Tracking number
   """
    response = getElta(tracking=tracking)
    return response


@ app.get("/v1/track/geniki/{tracking}", tags=["v1"], deprecated=True)
def trackGeniki(tracking):
    """Tracks Geniki Taxidromiki Courier vouchers 

    Parameters:
    tracking (str): Tracking number
   """
    response = getGeniki(tracking=tracking)
    return response
