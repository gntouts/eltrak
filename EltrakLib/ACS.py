from EltrakLib.BaseClasses import InvalidTrackingNumber, CourierTracker, TrackingCheckpoint, TrackingResult, format_timestamp
from requests import post, get
from string import digits
from bs4 import BeautifulSoup
from datetime import datetime


class AcsTracker(CourierTracker):
    """Tracker object for Speedex tracking numbers`"""
    courier = 'acs'
    base_url = 'https://api.acscourier.net/api/parcels/search/'
    allowed = digits

    def sanitize(self, tracking_number: str) -> str:
        '''Attempts to sanitize the given tracking number according to ELTA format'''
        new = ''.join([i for i in str(tracking_number)
                      if i in self.allowed])
        if len(new) != 10:
            raise InvalidTrackingNumber(
                message='ACS Tracking Numbers must contain 10 digits.')
        return new

    def fetch_results(self, tracking_number: str) -> dict:
        '''Requests tracking information for the given tracking number'''
        results = get(self.base_url+str(tracking_number))
        return results.json()['items'][0]

    def parse_results(self, tracking_info):
        '''Parses the results into useable information'''

        def parse_checkpoint(checkpoint):
            try: 
                if checkpoint['info'] == ' ':
                    status = checkpoint['description']
                else:
                    status = checkpoint['description'] + ' - ' + checkpoint['info']
            except:
                status = checkpoint['description'] 
            timestamp = checkpoint['controlPointDate'].split('.')[0]
            time = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')
            time = time.strftime('%d/%m/%Y στις %H:%M')
            space = checkpoint['controlPoint']
            return TrackingCheckpoint(status, time, space,
                format_timestamp(datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')))

        updates = [parse_checkpoint(update) for update in tracking_info['statusHistory']]
        last = sorted(updates, key=lambda k: k.datetime)[0]
        return TrackingResult(
            courier='ACS',
            tracking_number=tracking_info['trackingNumber'],
            updates=updates,
            delivered=tracking_info['isDelivered']
            )

    def track(self, tracking_number: str):
        tracking_number = self.sanitize(tracking_number)
        results = self.fetch_results(tracking_number)
        return self.parse_results(results)

    def track_silently(self, tracking_number: str):
        try:
            tracking_number = self.sanitize(tracking_number)
            results = self.fetch_results(tracking_number)
            return self.parse_results(results)
        except:
            return None
