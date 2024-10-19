

class MongoRepository:
    def __init__(self, mongo_conn, collection):
        self.__mongo_conn = mongo_conn[str(collection)]

    def upsert(self, filter, value):
        filter = {"id": filter.id}
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

    def remove(self, filter, field):
        self.__mongo_conn.update_one(
            {"id": filter.id},
            {"$unset": {field: ""}}
        )

    def get(self, id):
        filter = {"id": id}
        document = self.__mongo_conn.find_one(filter)
        return document
    
    def get_any(self, filter=None):
        documents = self.__mongo_conn.find(filter)
        return documents
    
    