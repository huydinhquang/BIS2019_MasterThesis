import pymongo as pym
import Controllers.SecretKeys as sk

def connect_mongodb():
    # Initialize connection.
    client = pym.MongoClient(**sk.mongo)
    db = client[sk.db_name]
    main_col = db[sk.collection_main_name]
    channel_col = db[sk.collection_channel_name]
    record_set_col  = db[sk.collection_record_set_name]
    return db, main_col, channel_col, record_set_col