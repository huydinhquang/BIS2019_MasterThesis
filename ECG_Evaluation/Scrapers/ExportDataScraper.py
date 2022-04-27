
from bson.objectid import ObjectId
import gridfs
import Controllers.ECGModel as ecg_model
import Controllers.Common as common
import Controllers.Constants as cons
from Controllers.FilesModel import Files
from Controllers.ECGModel import ECG
from datetime import datetime
import ECG_Evaluation.Scraper as scraper

def find_channel_list(my_col, query_data):
    match_query = {
        cons.CONS_ID_SHORT: query_data[cons.CONS_ID_SHORT]
    }

    lookup_query = {
        cons.CONS_QUERY_FROM: query_data[cons.CONS_QUERY_FROM],
        cons.CONS_QUERY_LOCALFIELD: query_data[cons.CONS_QUERY_LOCALFIELD],
        cons.CONS_QUERY_FOREIGNFIELD: query_data[cons.CONS_QUERY_FOREIGNFIELD],
        cons.CONS_QUERY_AS: query_data[cons.CONS_QUERY_AS]
    }

    query_data = {
        cons.CONS_QUERY_MATCH_QUERY:match_query,
        cons.CONS_QUERY_LOOKUP_QUERY:lookup_query
    }
    output = scraper.find_with_aggregate(my_col,query_data)
    
    return output
