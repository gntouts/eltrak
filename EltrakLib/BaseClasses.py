from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import List


def format_timestamp(input_date: datetime):
    temp = input_date.timestamp()
    temp = str(temp).split('.')[0]
    return temp

class InvalidTrackingNumber(ValueError):
    """Custom error raised when the input tracking number is invalid"""

    def __init__(self, message):
        self.message = message
        super().__init__()


@dataclass
class TrackingCheckpoint:
    """Representation of a tracking checkpoint"""
    status: str
    time: str
    space: str
    datetime: str


@dataclass
class TrackingResult:
    """Representation of the tracking results"""
    courier: str
    tracking_number: str
    updates: List[TrackingCheckpoint]
    found: bool = field(init=False)
    delivered: bool
    last: TrackingCheckpoint = field(init=False)

    def __post_init__(self):
        self.found = False
        self.last = None
        if len(self.updates) > 0:
            self.found = True
            self.last = sorted(self.updates, key=lambda k: k.datetime)[-1]
            if 'παραδόθηκε' in self.last.status.lower() or 'παραδοθηκε' in self.last.status.lower():
                self.delivered = True


class CourierTracker(ABC):
    '''Basic representation of a tracker.'''

    @abstractmethod
    def sanitize(self, tracking_number: str):
        '''Attempts to sanitize the given tracking number'''

    @abstractmethod
    def fetch_results(self, tracking_number: str):
        '''Requests tracking information for the given tracking number'''

    @abstractmethod
    def parse_results(self, tracking_info):
        '''Parses the results of the given tracking number'''

    @abstractmethod
    def track(self, tracking_number: str):
        '''Tracks the given tracking number'''

    @abstractmethod
    def track_silently(self, tracking_number: str):
        '''Attempts to track the given tracking number without throwing exceptions in case of failure'''
