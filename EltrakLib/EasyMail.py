from EltrakLib.BaseClasses import InvalidTrackingNumber, CourierTracker, TrackingCheckpoint, TrackingResult, format_timestamp
from bs4 import BeautifulSoup, element
from requests import get
from string import digits
from datetime import datetime


class EasyMailTracker(CourierTracker):
    """Tracker object for EasyMail tracking numbers`"""
    courier = 'easymail'
    base_url = 'https://trackntrace.easymail.gr/'
    allowed = digits

    def sanitize(self, tracking_number: str) -> str:
        '''Attempts to sanitize the given tracking number according to EasyMail format'''
        new = ''.join([i for i in str(tracking_number)
                      if i in self.allowed])
        if len(new) != 11:
            raise InvalidTrackingNumber(
                message='EasyMail Tracking Numbers must contain 11 digits.')
        return new

    def fetch_results(self, tracking_number: str) -> BeautifulSoup:
        '''Requests tracking information for the given tracking number'''
        results = get(self.base_url+str(tracking_number))
        return BeautifulSoup(results.text, features="html.parser")

    def parse_results(self, tracking_info, tracking_number):
        '''Parses the results into useable information'''

        def parse_checkpoint(checkpoint):
            timestamp = datetime.strptime(checkpoint.contents[3].contents[0][:-3], '%d/%m/%Y %H:%M:%S')
            date = timestamp.strftime('%d/%m/%Y στις %H:%M')
            description = str(checkpoint.contents[5].contents[0])
            location = checkpoint.contents[7].contents[0]
            if isinstance(location, element.Tag):
                # The last location update on a delivered package is a hyperlink, so I need to get only the text from it
                location = str(location.contents[0])

            return TrackingCheckpoint(description, date, location, 
                format_timestamp(timestamp))

        updates = [parse_checkpoint(update) for update in tracking_info.find_all("tbody")[-1].contents if update != "\n"]
        return TrackingResult(
            courier='EasyMail',
            tracking_number=tracking_number,
            updates=updates,
            delivered=updates[0].status == "Παραδόθηκε"
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
