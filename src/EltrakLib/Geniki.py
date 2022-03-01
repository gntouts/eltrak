from datetime import datetime
from string import digits
from requests import get
from bs4 import BeautifulSoup
from EltrakLib.BaseClasses import InvalidTrackingNumber, CourierTracker, TrackingCheckpoint, TrackingResult, format_timestamp


class GenikiTracker(CourierTracker):
    """Tracker object for Geniki tracking numbers`"""
    courier = 'geniki'
    base_url = 'https://www.taxydromiki.com/track/'
    allowed = digits

    def sanitize(self, tracking_number: str) -> str:
        '''Attempts to sanitize the given tracking number according to Geniki format'''
        new = ''.join([i for i in str(tracking_number)
                      if i in self.allowed])
        if len(new) != 10:
            raise InvalidTrackingNumber(
                message='Geniki Tracking Numbers must contain 10 digits.')
        return new

    def fetch_results(self, tracking_number: str) -> dict:
        '''Requests tracking information for the given tracking number'''
        results = BeautifulSoup(
            get(self.base_url+str(tracking_number)).text, features="html.parser")
        self.last_tracked = tracking_number
        return results

    def parse_results(self, tracking_info: BeautifulSoup) -> dict:
        '''Parses the results into useable information'''

        def parse_checkpoint(checkpoint: BeautifulSoup):
            description = checkpoint.find(
                attrs={"class": "checkpoint-status"}).get_text().replace('Κατάσταση', '')

            date = checkpoint.find(
                attrs={"class": "checkpoint-date"}).get_text().replace('Ημερομηνία', '')
            date = date.split(',')[-1].strip()
            dtime = checkpoint.find(
                attrs={"class": "checkpoint-time"}).get_text().replace('Ώρα', '')
            date = date + ' στις ' + dtime
            timestamp = datetime.strptime(date, '%d/%m/%Y στις %H:%M')

            location = checkpoint.find(attrs={"class": "checkpoint-location"})
            if location is not None:
                location = location.get_text().replace('Τοποθεσία', '')
            else:
                location = ""

            return TrackingCheckpoint(description, date, location, format_timestamp(timestamp))

        updates = tracking_info.find(
            attrs={"class": "tracking-result-content"}).find_all(attrs={"class": "tracking-checkpoint"})
        tracking_number = self.last_tracked
        delivered = updates[-1].find(attrs={"class": "checkpoint-location"}) == None
        updates = [parse_checkpoint(update) for update in updates]
        return TrackingResult('Geniki', tracking_number, updates, delivered)

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
