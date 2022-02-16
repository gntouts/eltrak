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
            get(self.base_url+str(tracking_number)).text, features="html.parser")
        self.last_tracked = tracking_number
        return results

    def parse_results(self, tracking_info: BeautifulSoup) -> dict:
        '''Parses the results into useable  information'''

        def parse_checkpoint(checkpoint: BeautifulSoup):
            items = checkpoint.find("span", {"class": "font-small-3"}).contents[0].split(", ")
            timestamp = datetime.strptime(items[1], "%d/%m/%Y στις %H:%M")
            date = items[1]
            location = items[0]
            description = checkpoint.find("h4", {"class": "card-title"}).contents[0].text

            return TrackingCheckpoint(description, date, location, format_timestamp(timestamp))

        tracking_number = tracking_info.find(attrs={"id": "TxtConsignmentNumber"}).get('value')

        if tracking_info.find("div", {"class": "alert-warning"}):
            return TrackingResult('Speedex', tracking_number, [], False)

        package = tracking_info.find_all("div", {"class": "timeline-card"})
        delivered = package[-1].find("h4", {"class": "card-title"}).contents[0].text == "Η ΑΠΟΣΤΟΛΗ ΠΑΡΑΔΟΘΗΚΕ"
        updates = [parse_checkpoint(update) for update in package]
        return TrackingResult('Speedex', tracking_number, updates, delivered)

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
