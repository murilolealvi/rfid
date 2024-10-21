
from datetime import datetime

def now():
    return datetime.now().strftime("%d/%m/%Y %H:%M")

class Person:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.date_registered = now()
