import json
from bson.json_util import dumps, loads
from repositories.registry import MongoRepository
import numpy as np


class AuthenticationHandler:
    def __init__(self, connection, collection):
        self.connection = MongoRepository(connection, collection)

    def authenticate(self, value, attribute):
        document = self.connection.get(value, attribute)
        return loads(dumps(document))
    #change last_time

    def check(self, value):
        if (self.connection.get(value, "id")):
            return True
        return False

    def user_exists(self):
        if self.connection.distinct("id"):
            return True
        return False
    
    def all_users(self):
        users = list()
        tag_ids =  self.connection.distinct("id")
        for tag_id in tag_ids:
            user = loads(dumps(self.connection.get(tag_id, "id")))
            users.append([tag_id, user["name"], user["date_registered"]])
        return users
    


