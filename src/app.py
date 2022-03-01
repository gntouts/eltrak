from EltrakLib.TrackerFactory import get_factory, CourierNotSupportedError
from EltrakLib.BaseClasses import InvalidTrackingNumber
from EltrakLib.GuessCourier import brute_force_track
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from enum import Enum


app = FastAPI(title="eltrak",
              description="""**eltrak** intends to become a free to use API to get shipping status for Greek courier services.
              <br>Currently, it **only** supports **ACS, Elta Courier, Speedex Courier, Skroutz Last Mile and EasyMail**.
              Geniki Tachidromiki is also provided, but it has not been tested at all and has caused issues when deployed in
              infrastracture located outside of Greece. Due to lack of tracking numbers in a variety of states
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
    skroutz = "skroutz"
    easymail = "easymail"
    geniki = "geniki"


@ app.get("/")
def general():
    return {"Project": "eltrak", "Repository": "https://github.com/gntouts/eltrak", "Documentation": "/documentation"}


@app.get('/v2/track-all/{tracking_number}', tags=["v2"])
def brute_force_track_courier(tracking_number: str):
    try:
        result = brute_force_track(tracking_number)
        if result:
            return result
        raise ValueError
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Couldn't find a tracking result",
            headers={
                "X-Error": "CourierNotSupportedError or InvalidTrackingNumber"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'Unknow error: {str(e)}. Please provide more details for debugging.',
            headers={"X-Error": "UnkownError"},
        )


@app.get('/v2/track/{courier}/{tracking_number}', tags=["v2"])
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
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'Unknow error: {str(e)}. Please provide more details for debugging.',
            headers={"X-Error": "UnkownError"},
        )
