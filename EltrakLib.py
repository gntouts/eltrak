from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List
from bs4 import BeautifulSoup
from requests import get
from string import digits
from datetime import datetime


class InvalidTrackingNumber(ValueError):
    """Custom error raised when the input tracking number is invalid"""

    def _init_(self, message):
        self.message = message
        super().init()


@dataclass
class TrackingCheckpoint:
    """Representation of a tracking checkpoint"""
    status: str
    time: str
    space: str
    datetime: datetime


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


class CourierTracker(ABC):
    '''Basic representation of a tracker.'''

    @abstractmethod
    def sanitize(self, tracking_number: str):
        '''Attempts to sanitize the given tracking number'''

    @abstractmethod
    def fetch_results(self, tracking_number: str):
        '''Requests tracking information for the given tracking number'''

    @abstractmethod
    def parse_results(self, tracking_info: BeautifulSoup):
        '''Parses the results of the given tracking number'''

    @abstractmethod
    def track(self, tracking_number: str):
        '''Tracks the given tracking number'''


class SpeedexTracker(CourierTracker):
    """Tracker object for Speedex tracking numbers`"""
    courier = 'speedex'
    base_url = 'http://speedex.gr/speedex/NewTrackAndTrace.aspx?number='

    def sanitize(self, tracking_number: str) -> str:
        '''Attempts to sanitize the given tracking number according to Speedex format'''
        new = ''.join([i for i in str(tracking_number) if i in digits])
        if len(new) != 12:
            raise InvalidTrackingNumber(
                'Speedex Tracking Numbers must contain 12 digits.')
        return new

    def fetch_results(self, tracking_number: str) -> BeautifulSoup:
        '''Requests tracking information for the given tracking number'''
        results = BeautifulSoup(
            get(self.base_url+str(tracking_number)).text, "lxml")
        return results

    def parse_results(self, tracking_info: BeautifulSoup) -> dict:
        '''Parses the results into useable  information'''

        def parse_checkpoint(checkpoint):
            status = checkpoint.find(
                'h4').get_text().replace('  ', ' ')
            timespace = checkpoint.find(
                attrs={"class": "font-small-3"}).get_text()
            time = timespace.split(',')[-1].strip()
            space = timespace.split(',')[0].strip()
            return TrackingCheckpoint(status, time, space,
                                      datetime.strptime(time, '%d/%m/%Y στις %H:%M'))

        def parse_delivered_checkpoint(checkpoint):
            if checkpoint:
                status = checkpoint.find('p').text
                timespace = checkpoint.find(
                    attrs={"class": "font-small-3"}).get_text()
                time = timespace.split(',')[-1].strip()
                space = timespace.split(',')[0].strip()
                return TrackingCheckpoint(status, time, space,
                                          datetime.strptime(time, '%d/%m/%Y στις %H:%M'))

        updates = tracking_info.find_all(attrs={"class": "timeline-item"})
        updates = [parse_checkpoint(update) for update in updates]
        delivered = tracking_info.find(attrs={"class": "delivered-speedex"})
        delivered = parse_delivered_checkpoint(delivered)
        tracking_number = tracking_info.find(
            attrs={"id": "TxtConsignmentNumber"}).get('value')
        delivered_flag = False
        if delivered:
            delivered_flag = True
            updates.append(delivered)
        found = True if len(updates) > 0 else False
        return TrackingResult(
            'Speedex', tracking_number, updates, delivered_flag)

    def track(self, tracking_number: str):
        tracking_number = self.sanitize(tracking_number)
        soup_results = self.fetch_results(tracking_number)
        return self.parse_results(soup_results)
