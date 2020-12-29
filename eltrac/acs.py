import requests
from bs4 import BeautifulSoup
import datetime


class ACSOrder:
    def __init__(self, tracking):
        self.tracking = str(tracking)
        self.url = 'https://www.acscourier.net/el/track-and-trace?p_p_id=ACSCustomersAreaTrackTrace_WAR_ACSCustomersAreaportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-4&p_p_col_count=1&_ACSCustomersAreaTrackTrace_WAR_ACSCustomersAreaportlet_stop_mobile=yes&_ACSCustomersAreaTrackTrace_WAR_ACSCustomersAreaportlet_jspPage=TrackTraceController&stop_mobile=yes'
        self.courier = 'ACS'

    def track(self):
        if len(self.tracking) != 10:
            self.result = 'Invalid tracking number'
        else:
            postData = {'generalCode': self.tracking}
            soup = BeautifulSoup(requests.post(
                self.url, data=postData).content, "lxml")
            scripts = soup.find_all('script')
            jqScripts = []
            for each in scripts:
                t = str(each)
                if 'grid.jqGrid' in t and 'addRowData' in t:
                    jqScripts.append(each)
            if len(jqScripts) == 1:
                script = jqScripts[0]
            else:
                script = None

            if script:
                updates = []
                rows = str(script).split('_r={rows:')[-1].split(';')[0]
                rows = rows.replace('id', '"id"').replace(
                    'cell', '"cell"')[:-1]
                for row in rows:
                    state = row['cell']
                    temp = {}
                    temp['status'] = state[1]
                    temp['time'] = state[0].split(' ')[-1][:-3]
                    temp['space'] = state[2]
                    temp['datetime'] = datetime.datetime.strptime(
                        state[0][:-3], '%d/%m/%Y %H:%M')
                    updates.append(temp)
                if len(updates) > 0:
                    self.results = updates
                else:
                    self.results = 'No data'
            else:
                self.results = 'No data'
