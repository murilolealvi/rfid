from pymongo import MongoClient
from .database import connections



class MongodbConnectionHandler:
    def __init__(self, db):
        self.__host = connections['MONGODB']['HOST']
        self.__port = connections['MONGODB']['PORT']
        self.__db = db
        self.__conn = None

    def connect(self):
        self.__conn= MongoClient(
            host=self.__host,
            port=self.__port,
        )
        return self.__conn[str(self.__db)]

    def get_conn(self):
        return self.__conn