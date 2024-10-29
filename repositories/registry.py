

class MongoRepository:
    def __init__(self, mongo_conn, collection):
        self.__mongo_conn = mongo_conn[str(collection)]

    def insert(self, object):
        self.__mongo_conn.insert_one(object)

    def upsert(self, filter, value, attribute="id"):
        filter = {attribute : filter.id}
        self.__mongo_conn.update_one(
            filter,
            {"$set": value},
            upsert=True
        )

    def push(self, filter, value, array):
        self.__mongo_conn.update_one(
            {"id": filter.id},
            {"$push": {array: value}}
        )

    def pull(self, filter, value, array):
        self.__mongo_conn.update_one(
            {"id": filter.id},
            {"$pull": {array : value}}
        )

    def remove(self, value):
        filter = {"id": value}
        self.__mongo_conn.delete_one(filter)

    def get(self, value, attribute):
        filter = {f"{attribute}": value}
        document = self.__mongo_conn.find_one(filter)
        return document
    
    def distinct(self, field):
        return self.__mongo_conn.distinct(field)
    
    