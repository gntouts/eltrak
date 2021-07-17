from EltrakLib.BaseClasses import InvalidTrackingNumber, CourierTracker, TrackingCheckpoint, TrackingResult
from requests import post
from string import digits
from bs4 import BeautifulSoup
from datetime import datetime


class AcsTracker(CourierTracker):
    """Tracker object for Speedex tracking numbers`"""
    courier = 'acs'
    base_url = 'https://www.acscourier.net/el/track-and-trace?p_p_id=ACSCustomersAreaTrackTrace_WAR_ACSCustomersAreaportlet&\
                p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-4&p_p_col_count=1&\
                _ACSCustomersAreaTrackTrace_WAR_ACSCustomersAreaportlet_stop_mobile=yes\
                &_ACSCustomersAreaTrackTrace_WAR_ACSCustomersAreaportlet_jspPage=TrackTraceController&stop_mobile=yes'
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
        post_data = {'generalCode': tracking_number}
        results = BeautifulSoup(
            post(self.base_url, data=post_data).content, "lxml")
        self.last_tracked = tracking_number
        return results

    def parse_results(self, tracking_info):
        '''Parses the results into useable information'''

        def parse_checkpoint(checkpoint):
            checkpoint = checkpoint['cell']
            status = checkpoint[1]
            time = checkpoint[0].split(' ')[0]\
                + ' στις ' + checkpoint[0].split(' ')[-1][:-3]
            space = checkpoint[2]
            return TrackingCheckpoint(status, time, space,
                                      datetime.strptime(checkpoint[0][:-3], '%d/%m/%Y %H:%M'))

        scripts = [str(i) for i in tracking_info.find_all(
            'script') if ('grid.jqGrid' in i and 'addRowData' in i)]
        script = scripts[0] if len(scripts) == 1 else None
        if script:
            checkpoint_obj = str(script).split('_r={rows:')[-1].split(';')[0]
            checkpoint_obj = checkpoint_obj.replace('id', '"id"').replace(
                'cell', '"cell"')[:-1]
            updates = eval(checkpoint_obj)
            updates = [parse_checkpoint(checkpoint)
                       for checkpoint in updates]
            if len(updates > 0):
                return TrackingResult('ACS', self.last_tracked, updates, False)
        return TrackingResult('ACS', self.last_tracked, [], False)

    def track(self, tracking_number: str):
        tracking_number = self.sanitize(tracking_number)
        results = self.fetch_results(tracking_number)
        return self.parse_results(results)
