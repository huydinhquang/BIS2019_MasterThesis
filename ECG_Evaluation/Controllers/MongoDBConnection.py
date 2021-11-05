import pymongo as pym
import Controllers.SecretKeys as sk

def connect_mongodb():
    # Initialize connection.
    client = pym.MongoClient(**sk.mongo)
    return client[sk.db_name]

def connect_mongo_collectiondb():
    db = connect_mongodb()
    return db[sk.collection_name]