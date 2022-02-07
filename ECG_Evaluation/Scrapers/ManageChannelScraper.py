
from bson.objectid import ObjectId
import gridfs
import Controllers.ECGModel as ecg_model
import Controllers.Common as common
import Controllers.Constants as cons
from Controllers.FilesModel import Files
from Controllers.ECGModel import ECG
from datetime import datetime

def add_channel(my_col, new_channel):
    current_date = datetime.now()
    new_channel_json = {cons.CONS_CHANNEL: new_channel,
                        cons.CONS_CREATED_DATE: current_date, cons.CONS_MODIFIED_DATE: current_date}
    output = my_col.insert_one(new_channel_json)
    if output:
        print('channel_id: ' + str(output))
    return output.inserted_id
