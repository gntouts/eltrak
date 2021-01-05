import requests
from bs4 import BeautifulSoup
import datetime



class GenikiOrder:
    def __init__(self, tracking):
        self.tracking = str(tracking)
        self.url = 'https://www.taxydromiki.com/track/{}'.format(
            self.tracking)
        self.courier = 'Geniki Taxydromiki'

    def track(self):
        if len(self.tracking) < 9:
            self.result = 'Invalid tracking number'
        else:
            soup = BeautifulSoup(requests.get(self.url).text, "lxml")
            container = soup.find(attrs={"class": "tracking-result-content"})
            updates = container.find_all(attrs={"class": "tracking-checkpoint"})
            if len(updates) > 0:
                steps = []
                print(container, updates)
                for update in updates:
                    temp = {}
                    temp['status'] = update.find(attrs={"class": "checkpoint-status"}).get_text().replace('Κατάσταση', '')
                    temp['space'] = update.find(attrs={"class": "checkpoint-location"}).get_text().replace('Τοποθεσία', '')
                    date =  update.find(attrs={"class": "checkpoint-date"}).get_text().replace('Ημερομηνία', '')
                    date = date.split(',')[-1].strip()
                    time = update.find(attrs={"class": "checkpoint-time"}).get_text().replace('Ώρα', '')
                    temp['time'] = date +' στις '+time
                    temp['datetime'] =  datetime.datetime.strptime(temp['time'], '%d/%m/%Y στις %H:%M')
                    steps.append(temp)
            if steps == []:
                self.result = 'No data'
            else:
                self.result = steps

new = GenikiOrder(700005806876)
new.track()