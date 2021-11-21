import pymongo as pym
import Controllers.SecretKeys as sk

def connect_mongodb():
    # Initialize connection.
    client = pym.MongoClient(**sk.mongo)
    db = client[sk.db_name]
    main_col = db[sk.collection_main_name]
    # channel_col = db[sk.collection_channel_name]
    return db, main_col