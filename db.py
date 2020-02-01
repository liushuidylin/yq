import pymongo


class DB:
    def __init__(self):
        self.mongodb_client = pymongo.MongoClient('localhost', 27017)
        self.db = self.mongodb_client.get_database('study')

    def insert(self, collection, data):
        self.db[collection].insert_one(data)

    def find_all(self):
        print(self.db.list_collection_names())

    def statistics_data(self, date):
        q = {"insertTime": date}
        return self.db['yq'].find(q)

    def find_one(self, q):
        return self.db['yq'].find_one(q)


if __name__ == '__main__':
    db = DB()
    new_date = '2020-02-01 00:00:00'
    old_date = '2020-01-31 00:00:00'
    data = db.statistics_data(new_date)
    new_data = ''
    for d in data:
        if 'cityName' in d:
            q = {"provinceName": d['provinceName'], "cityName": d['cityName'], "insertTime": old_date}
            new_data = db.find_one(q)
        else:
            q = {"provinceName": d['provinceName'], "insertTime": old_date}
            new_data = db.find_one(q)

        if new_data is None:
            pass
        else:
            d['confirmedCount'] = d['confirmedCount'] - new_data['confirmedCount']
            d['suspectedCount'] = d['suspectedCount'] - new_data['suspectedCount']
            d['curedCount'] = d['curedCount'] - new_data['curedCount']
            d['deadCount'] = d['deadCount'] - new_data['deadCount']
            db.insert('data3', d)
