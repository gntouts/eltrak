from requests.models import Response
from EltrakLib.TrackerFactory import get_factory, CourierNotSupportedError
from EltrakLib.BaseClasses import InvalidTrackingNumber
from EltrakLib.deprecation_support import DeprecatedTrackingResult
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from enum import Enum

# deprecated
from EltrakLib.geniki import GenikiOrder

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


@app.get('/v2/track/{courier}/{tracking_number}', tags=["v1"])
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


# ------------V1-------------


@ app.get("/v1/track/geniki/{tracking}", tags=["v1"], deprecated=True)
def trackGeniki(tracking):
    """Tracks Geniki Taxidromiki Courier vouchers 

    Parameters:
    tracking (str): Tracking number
   """
    geniki_tracker = GenikiOrder(tracking=tracking)
    response = geniki_tracker.get_result()
    return response


@app.get('/v1/track/{courier}/{tracking_number}', tags=["v1"], deprecated=True)
def deprecated_track_courier(courier: CourierName, tracking_number: str):
    try:
        courier = str(courier).split('.')[-1]
        factory = get_factory(courier)
        tracker = factory.get_tracker()
        result = tracker.track(tracking_number)
        return DeprecatedTrackingResult().from_result(result)
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
