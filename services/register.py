import json
from bson.json_util import dumps, loads

from repositories.registry import MongoRepository
from models.person import Person
from mongoengine import *


class RegisterHandler:
    def __init__(self, connection, collection):
        self.connection = MongoRepository(connection, collection)

    def register(self, object):
        document = self.__object_to_document(object)
        self.connection.upsert(object, document)

    def erase(self, person: Person):
        self.connection.remove(
            filter = person,
            field = f"rfid.{person.id}",
        )
    
    def __object_to_document(self, object):
        return json.loads(json.dumps(object, default= lambda o: o.__dict__))

