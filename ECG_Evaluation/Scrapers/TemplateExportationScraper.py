
from bson.objectid import ObjectId
import gridfs
import Controllers.ECGModel as ecg_model
import Controllers.Common as common
import Controllers.Constants as cons
from Controllers.FilesModel import Files
from Controllers.ECGModel import ECG
from datetime import datetime

def add_template(my_col, values):
    exp_tem_name = values[cons.CONS_EXPORTING_TEMPLATE_NAME]
    list_channel = values[cons.CONS_CHANNEL]
    target_sample_rate = values[cons.CONS_TARGET_SAMPLE_RATE]
    duration = values[cons.CONS_DURATION]

    current_date = datetime.now()
    new_template_json = {
        cons.CONS_EXPORTING_TEMPLATE_NAME: exp_tem_name,
        cons.CONS_CHANNEL: list_channel,
        cons.CONS_TARGET_SAMPLE_RATE: target_sample_rate,
        cons.CONS_DURATION: duration,
        cons.CONS_CREATED_DATE: current_date, 
        cons.CONS_MODIFIED_DATE: current_date
    }
    output = my_col.insert_one(new_template_json)
    if output:
        print('template_id: ' + str(output))
    return output.inserted_id
