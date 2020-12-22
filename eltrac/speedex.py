import requests
from bs4 import BeautifulSoup
import datetime
from pydantic import BaseModel
from typing import Optional


class Order(BaseModel):
    tracking: str
    courier: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "tracking": "700005728133",
                "courier": "Speedex",
                "updates": [{"status": "ΕΙΣΑΓΩΓΗ ΣΕ ΚΑΤΑΣΤΗΜΑ", "time": "21/12/2020 στις 18:48", "space": "ΠΑΤΡΑ  ΚΑΝΑΡΗ", "datetime": "2020-12-21T18:48:00"}, {"status": "ΠΑΡΑΛΑΒΗ ΑΠΟ ΠΕΛΑΤΗ", "time": "21/12/2020 στις 18:52", "space": "ΠΑΤΡΑ  ΚΑΝΑΡΗ", "datetime": "2020-12-21T18:52:00"}, {"status": "ΕΞΑΓΩΓΗ ΑΠΟ ΚΑΤΑΣΤΗΜΑ", "time": "21/12/2020 στις 23:40", "space": "ΠΑΤΡΑ  ΚΑΝΑΡΗ", "datetime": "2020-12-21T23:40:00"}, {"status": "ΕΙΣΑΓΩΓΗ ΣΕ Δ/Κ", "time": "21/12/2020 στις 23:41", "space": "ΔΙΑΜΕΤΑΚΟΜΙΣΤΙΚΟ ΚΕΝΤΡΟ ΑΙΓΙΟΥ", "datetime": "2020-12-21T23:41:00"}]
            }
        }


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
                self.result = steps
