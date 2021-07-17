import string
from EltrakLib.BaseClasses import InvalidTrackingNumber, CourierTracker, TrackingCheckpoint, TrackingResult
from requests import post
from json import loads
from string import digits, ascii_letters
from datetime import datetime


class EltaTracker(CourierTracker):
    """Tracker object for Speedex tracking numbers`"""
    courier = 'elta courier'
    base_url = 'https://www.elta-courier.gr/track.php'
    allowed = digits + ascii_letters

    def sanitize(self, tracking_number: str) -> str:
        '''Attempts to sanitize the given tracking number according to ELTA format'''
        new = ''.join([i for i in str(tracking_number)
                      if i in self.allowed])
        if len(new) < 10:
            raise InvalidTrackingNumber(
                message='ELTA Tracking Numbers must contain at least 10 charactes.')
        return new

    def fetch_results(self, tracking_number: str) -> dict:
        '''Requests tracking information for the given tracking number'''
        post_data = {'number': tracking_number}
        res = post(self.base_url, data=post_data).content
        self.last_tracked = tracking_number
        return loads(res)['result']

    def parse_results(self, tracking_info):
        '''Parses the results into useable information'''

        def parse_checkpoint(checkpoint):
            status = checkpoint['status']
            time = checkpoint['date'].replace('-', '/') \
                + ' στις ' + checkpoint['time']
            space = checkpoint['place']
            return TrackingCheckpoint(status, time, space, datetime.strptime(
                checkpoint['date']+' '+checkpoint['time'], '%d-%m-%Y %H:%M'))

        for key in tracking_info.keys():
            tracking_number = key
        tracking_info = tracking_info[tracking_number]['result']
        if tracking_info == "wrong number":
            return TrackingResult('ELTA Courier', tracking_number, [], False)
        updates = [parse_checkpoint(update) for update in tracking_info]
        return TrackingResult('ELTA Courier', tracking_number, updates, False)

    def track(self, tracking_number: str):
        tracking_number = self.sanitize(tracking_number)
        results = self.fetch_results(tracking_number)
        return self.parse_results(results)
