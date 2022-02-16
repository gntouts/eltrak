from EltrakLib.BaseClasses import InvalidTrackingNumber, CourierTracker, TrackingCheckpoint, TrackingResult, format_timestamp
from requests import get
from string import digits
from bs4 import BeautifulSoup
from datetime import datetime


class SpeedexTracker(CourierTracker):
    """Tracker object for Speedex tracking numbers`"""
    courier = 'speedex'
    base_url = 'http://speedex.gr/speedex/NewTrackAndTrace.aspx?number='
    allowed = digits

    def sanitize(self, tracking_number: str) -> str:
        '''Attempts to sanitize the given tracking number according to Speedex format'''
        new = ''.join([i for i in str(tracking_number) if i in self.allowed])
        if len(new) != 12:
            raise InvalidTrackingNumber(
                message='Speedex Tracking Numbers must contain 12 digits.')
        return new

    def fetch_results(self, tracking_number: str) -> BeautifulSoup:
        '''Requests tracking information for the given tracking number'''
        results = BeautifulSoup(
            get(self.base_url+str(tracking_number)).text, "lxml")
        self.last_tracked = tracking_number
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
                                      format_timestamp(datetime.strptime(time, '%d/%m/%Y στις %H:%M')))

        def parse_delivered_checkpoint(checkpoint):
            if checkpoint:
                status = checkpoint.find('p').text
                timespace = checkpoint.find(
                    attrs={"class": "font-small-3"}).get_text()
                time = timespace.split(',')[-1].strip()
                space = timespace.split(',')[0].strip()
                return TrackingCheckpoint(status, time, space,
                                          format_timestamp(datetime.strptime(time, '%d/%m/%Y στις %H:%M')))

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

    def track_silently(self, tracking_number: str):
        try:
            tracking_number = self.sanitize(tracking_number)
            results = self.fetch_results(tracking_number)
            return self.parse_results(results)
        except:
            return None