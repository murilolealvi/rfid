
from datetime import datetime

def now():
    date = datetime.now().strftime("%d/%m/%Y")
    time = datetime.now().strftime("%H:%M:%S")
    return date, time

class Log:
    def __init__(self, name):
        date, time = now()
        self.name = name
        self.date = date
        self.time = time
