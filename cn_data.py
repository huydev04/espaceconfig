from pymongo import MongoClient 

def cndb():
    url = 'mongodb://localhost:27017/'
    client = MongoClient(url)
    print(client['espacedb'])
    db = client['espacedb']
    return db


