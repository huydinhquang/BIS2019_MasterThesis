import pymongo as pym
import Controllers.SecretKeys as sk
import Controllers.Constants as cons

def connect_mongodb():
    # Initialize connection.
    client = pym.MongoClient(**sk.mongo)
    db = client[sk.db_name]
    ecg_col = db[sk.collection_ecg_name]
    channel_col = db[sk.collection_channel_name]
    record_set_col  = db[sk.collection_record_set_name]
    template_exportation_col  = db[sk.collection_exporting_template_name]

    result = {
        cons.DB_NAME: db,
        cons.COLLECTION_ECG_NAME: ecg_col,
        cons.COLLECTION_CHANNEL_NAME: channel_col,
        cons.COLLECTION_RECORD_SET_NAME: record_set_col,
        cons.COLLECTION_EXPORTING_TEMPLATE_NAME: template_exportation_col
    }

    return result