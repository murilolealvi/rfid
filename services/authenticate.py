
from bson.json_util import dumps, loads
from repositories.registry import MongoRepository
from models.person import Person


class AuthenticationHandler:
    def __init__(self, connection):
        collection = "database"
        self.connection = MongoRepository(connection, collection)

    def authenticate(self, id):
        document = self.connection.get(id)
        return loads(dumps(document))
    #change last_time

