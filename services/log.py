
from bson.json_util import dumps, loads
from repositories.registry import MongoRepository
import json

class LogHandler:
    def __init__(self, connection, collection):
        self.connection = MongoRepository(connection, collection)

    def find(self, time):
        return self.connection.get(time, "time")
    
    def log(self, object):
        document = self.__object_to_document(object)
        self.connection.insert(document)

    def dump(self):
        logs = list()
        times = self.connection.distinct("time")
        for time in times[::-1]:
            user = loads(dumps(self.connection.get(time, "time")))
            logs.append([user["name"], user["date"], time])
        return logs
    
    def log_exists(self):
        if self.connection.distinct("name"):
            return True
        return False
    
    def __object_to_document(self, object):
        return json.loads(json.dumps(object, default= lambda o: o.__dict__))
    
    @property
    def timelogs(self):
        return self.connection.distinct("time")

    