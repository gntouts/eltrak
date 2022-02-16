from EltrakLib.BaseClasses import InvalidTrackingNumber, CourierTracker, TrackingCheckpoint, TrackingResult, format_timestamp
from requests import get
from string import digits, ascii_uppercase
from datetime import datetime


class SkroutzTracker(CourierTracker):
    """Tracker object for Skroutz Last Mile tracking numbers`"""
    courier = 'acs'
    base_url = 'https://api.sendx.gr/user/hp/'
    allowed = digits + ascii_uppercase

    def sanitize(self, tracking_number: str) -> str:
        '''Attempts to sanitize the given tracking number according to Skroutz Last Mile format'''
        new = ''.join([i for i in str(tracking_number)
                      if i in self.allowed])
        if len(new) != 13:
            raise InvalidTrackingNumber(
                message='Skroutz Last Mile Tracking Numbers must contain 13 digits or uppercase letters.')
        return new

    def fetch_results(self, tracking_number: str) -> dict:
        '''Requests tracking information for the given tracking number'''
        results = get(self.base_url+str(tracking_number))
        return results.json()

    def parse_results(self, tracking_info, tracking_number):
        '''Parses the results into useable information'''

        def parse_checkpoint(checkpoint):
            timestamp = checkpoint['createdAt'][:-5]
            tdate = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')
            date = tdate.strftime('%d/%m/%Y στις %H:%M')
            location = checkpoint['driver']['city'] if checkpoint['driver'] else "Unknown"
            status = checkpoint['description']

            return TrackingCheckpoint(status, date, location,
                format_timestamp(datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')))

        updates = [parse_checkpoint(update) for update in tracking_info['trackingDetails']]
        return TrackingResult(
            courier='Skroutz Last Mile',
            tracking_number=tracking_number,
            updates=updates,
            delivered=tracking_info['deliveredAt'] != None
            )

    def track(self, tracking_number: str):
        tracking_number = self.sanitize(tracking_number)
        results = self.fetch_results(tracking_number)
        return self.parse_results(results, tracking_number)

    def track_silently(self, tracking_number: str):
        try:
            tracking_number = self.sanitize(tracking_number)
            results = self.fetch_results(tracking_number)
            return self.parse_results(results, tracking_number)
        except:
            return None
