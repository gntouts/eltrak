from EltrakLib.ACS import AcsTracker
from EltrakLib.ELTA import EltaTracker
from EltrakLib.Speedex import SpeedexTracker
from abc import ABC, abstractclassmethod


class CourierNotSupportedError(NotImplementedError):
    def __init__(self, courier):
        self.message = f'{courier} courier is not yet supported or non existent.'
        super().__init__()


class TrackerFactory(ABC):
    @ abstractclassmethod
    def get_tracker(self):
        """Returns a tracker instance"""


class AcsFactory(TrackerFactory):
    def get_tracker(self):
        return AcsTracker()


class EltaFactory(TrackerFactory):
    def get_tracker(self):
        return EltaTracker()


class SpeedexFactory(TrackerFactory):
    def get_tracker(self):
        return SpeedexTracker()


def get_factory(name):
    factories = {
        'acs': AcsFactory(),
        'speedex': SpeedexFactory(),
        'elta': EltaFactory()
    }
    sanitized_name = str(name).lower()
    if sanitized_name in factories:
        return factories[sanitized_name]
    else:
        raise CourierNotSupportedError(sanitized_name)
