from eltrac import speedex, acs, elta


def getSpeedex(tracking):
    temp = speedex.SpeedexOrder(tracking=tracking)
    temp.track()
    return {'courier': temp.courier, 'tracking': temp.tracking, 'updates': temp.result}


def getACS(tracking):
    temp = acs.ACSOrder(tracking=tracking)
    temp.track()
    return {'courier': temp.courier, 'tracking': temp.tracking, 'updates': temp.result}


def getElta(tracking):
    temp = elta.EltaOrder(tracking=tracking)
    temp.track()
    return {'courier': temp.courier, 'tracking': temp.tracking, 'updates': temp.result}
