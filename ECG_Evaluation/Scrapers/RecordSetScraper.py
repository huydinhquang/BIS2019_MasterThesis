
from bson.objectid import ObjectId
import gridfs
import Controllers.ECGModel as ecg_model
import Controllers.Common as common
import Controllers.Constants as cons
from Controllers.FilesModel import Files
from Controllers.ECGModel import ECG
from datetime import datetime

def add_record_set(my_col, record_set_name, list_source):
    current_date = common.get_current_date()
    new_record_set_json = {
        cons.CONS_RECORD_SET_NAME: record_set_name,
        cons.ECG_SOURCE: list_source,
        cons.CONS_CREATED_DATE: current_date, 
        cons.CONS_MODIFIED_DATE: current_date
    }
    output = my_col.insert_one(new_record_set_json)
    if output:
        print('record_set_id: ' + str(output))
    return output.inserted_id
