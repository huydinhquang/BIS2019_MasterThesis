
from bson.objectid import ObjectId
import gridfs
import Controllers.ECGModel as ecg_model
import Controllers.Common as common
import Controllers.Constants as cons
from Controllers.FilesModel import Files
from Controllers.ECGModel import ECG
from datetime import datetime

def add_template(my_col, target_sample_rate, duration, list_channel):
    # TODO
    current_date = datetime.now()
    new_template_json = {
        cons.CONS_CHANNEL: list_channel,
        cons.CONS_CREATED_DATE: current_date, 
        cons.CONS_MODIFIED_DATE: current_date
    }
    output = my_col.insert_one(new_template_json)
    if output:
        print('template_id: ' + str(output))
    return output.inserted_id
