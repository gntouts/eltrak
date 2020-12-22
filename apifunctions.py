from eltrac import speedex


def getSpeedex(tracking):
    temp = speedex.SpeedexOrder(tracking=tracking)
    temp.track()
    return {'courier': temp.courier, 'tracking': temp.tracking, 'updates': temp.result}
