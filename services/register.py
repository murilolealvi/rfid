import json
from bson.json_util import dumps, loads

from repositories.registry import MongoRepository
from mongoengine import *


class RegisterHandler:
    def __init__(self, connection, collection):
        self.connection = MongoRepository(connection, collection)

    def register(self, object):
        document = self.__object_to_document(object)
        self.connection.upsert(object, document)

    def erase(self, value):
        self.connection.remove(value)
    
    def __object_to_document(self, object):
        return json.loads(json.dumps(object, default= lambda o: o.__dict__))

