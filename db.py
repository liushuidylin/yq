import pymongo


class DB:
    def __init__(self):
        self.mongodb_client = pymongo.MongoClient('47.95.112.185', 27017)
        self.db = self.mongodb_client.get_database('study')

    def insert(self, collection, data):
        self.db[collection].insert_one(data)

    def find_all(self):
        print(self.db.list_collection_names())


if __name__ == '__main__':
    db = DB()
    test_data = {
        'province': 'shanxi',
        'city': 'yuncheng',
        'confirmed': 2,
        'death': 0,
        'cured': 0,
        'suspect': 1
    }
    db.insert('yq', test_data)