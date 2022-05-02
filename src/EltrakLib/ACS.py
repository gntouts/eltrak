from EltrakLib.BaseClasses import InvalidTrackingNumber, CourierTracker, TrackingCheckpoint, TrackingResult, format_timestamp
from string import digits
from selenium import webdriver
from selenium.webdriver.firefox import options
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup as bs
from datetime import datetime

def setup_driver() -> webdriver:
    Options = options.Options()
    Options.headless = True

    driver = webdriver.Firefox(options=Options, service=Service(GeckoDriverManager().install()))
    return driver 

class AcsTracker(CourierTracker):
    """Tracker object for ACS tracking numbers`"""
    courier = 'acs'
    base_url = 'https://www.acscourier.net/el/web/greece/track-and-trace?action=getTracking3&generalCode='
    allowed = digits
    driver = setup_driver()

    def sanitize(self, tracking_number: str) -> str:
        '''Attempts to sanitize the given tracking number according to ACS format'''
        new = ''.join([i for i in str(tracking_number)
                      if i in self.allowed])
        if len(new) != 10:
            raise InvalidTrackingNumber(
                message='ACS Tracking Numbers must contain 10 digits.')
        return new

    def fetch_results(self, tracking_number: str) -> dict:
        '''Requests tracking information for the given tracking number'''
        self.driver.get(self.base_url+str(tracking_number))

        try:
           WebDriverWait(self.driver, 8).until(EC.visibility_of_element_located((By.TAG_NAME, 'app-parcels-search-results'))) 
        except TimeoutException:
            return None

        results = bs(self.driver.page_source, features="html.parser")
        return results

    def parse_results(self, tracking_info: bs, tracking_number):
        '''Parses the results into useable information'''

        def parse_checkpoint(checkpoint):
            details = checkpoint.find_all("td")
            dt = details[1].text
            dt = dt.replace('μ.μ.', 'PM')   # They are using 12-hour format so I have to specify AM / PM
            dt = dt.replace('π.μ.', 'AM')

            try:
                timestamp = datetime.strptime(dt, ' %d/%m/%y, %I:%M %p ')
            except ValueError:  # No idea why, but sometimes this breaks
                timestamp = datetime.now()  # This can't be left empty, so for now I'm putting he current time until a better solution can be found

            date = timestamp.strftime('%d/%m/%Y, %H:%M')
            return TrackingCheckpoint(
                details[2].text,
                date,
                details[0].text,
                format_timestamp(timestamp)
            )

        tables = tracking_info.find_all("tbody")
        tbody2 = tables[-1]     # To find if it's delivered
        tbody1 = tables[-2]     # To find everything else
        checkpoint_list = tbody2.find_all("tr")

        if len(checkpoint_list) == 0:   # Parcel not found
            return TrackingResult('ACS', tracking_number, [], False)

        updates = [parse_checkpoint(update) for update in checkpoint_list]

        return TrackingResult(
            courier='ACS',
            tracking_number=tracking_number,
            updates=updates,
            delivered=tbody1.find("tr", {"class": "delivered"}) != 0
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
