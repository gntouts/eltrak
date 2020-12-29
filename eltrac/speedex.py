import requests
from bs4 import BeautifulSoup
import datetime


class SpeedexOrder:
    def __init__(self, tracking):
        self.tracking = str(tracking)
        self.url = 'http://speedex.gr/speedex/NewTrackAndTrace.aspx?number={}'.format(
            self.tracking)
        self.courier = 'Speedex'

    def track(self):
        if len(self.tracking) != 12:
            self.result = 'Invalid tracking number'
        else:
            soup = BeautifulSoup(requests.get(self.url).text, "lxml")
            updates = soup.find_all(attrs={"class": "timeline-item"})
            final = None

            final = soup.find(attrs={"class": "delivered-speedex"})

            if final != None:
                tremp = final.find('p').text
                timespace = final.find(
                    attrs={"class": "font-small-3"}).get_text()
                time = timespace.split(',')[-1].strip()
                space = timespace.split(',')[0].strip()
                final = {'status': tremp, 'time': time, 'space': space, 'datetime': datetime.datetime.strptime(
                    time, '%d/%m/%Y στις %H:%M')}
            self.final = final
            steps = []
            for update in updates:
                temp = {}
                temp['status'] = update.find(
                    'h4').get_text().replace('  ', ' ')
                timespace = update.find(
                    attrs={"class": "font-small-3"}).get_text()
                time = timespace.split(',')[-1].strip()
                space = timespace.split(',')[0].strip()
                temp['time'] = time
                temp['space'] = space
                temp['datetime'] = datetime.datetime.strptime(
                    time, '%d/%m/%Y στις %H:%M')
                steps.append(temp)
            if steps == []:
                self.result = 'No data'
            else:
                if self.final != None:
                    steps.append(self.final)
                self.result = steps
