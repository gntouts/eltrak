from bs4.element import DEFAULT_OUTPUT_ENCODING
import requests
from bs4 import BeautifulSoup
import datetime
import json


class EltaOrder:
    def __init__(self, tracking):
        self.tracking = str(tracking)
        self.courier = 'Elta Courier'
        self.url = 'https://www.elta-courier.gr/track.php'

    def track(self):
        if len(self.tracking) < 10:
            self.result = 'Invalid tracking number'
        else:
            postData = {'number': self.tracking}
            try:
                response = requests.post(self.url, data=postData).content
                response = json.loads(response)
                states = response['result'][self.tracking]['result']
                if states != 'wrong number':
                    updates = []
                    for state in states:
                        temp = {}
                        temp['status'] = state['status']
                        temp['time'] = state['date'].replace(
                            '-', '/') + ' στις ' + state['time']
                        temp['space'] = state['place']
                        temp['datetime'] = datetime.datetime.strptime(
                            state['date']+' '+state['time'], '%d-%m-%Y %H:%M')
                        updates.append(temp)
                    if len(updates) > 0:
                        self.result = updates
                    else:
                        self.result = 'No data!'
                else:
                    self.result = 'No data!'
            except:
                self.result = 'Application Error'


new = EltaOrder('NP220212591GR')
