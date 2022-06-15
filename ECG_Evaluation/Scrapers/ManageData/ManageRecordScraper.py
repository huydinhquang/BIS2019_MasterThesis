import Controllers.Common as common
import Controllers.Constants as cons
from Controllers.ECGModel import ECG
import Scraper as scraper

def update_record(ecg_col, field_name, item_id, list_new_values: ECG):
    jsonecg_propertyStr = common.parse_json(list_new_values.__dict__)
    # Get current date
    current_date = common.get_current_date()
    # Update Created date and Modified date with the Date Type (This is used to handle the Date type in MongoDB)
    jsonecg_propertyStr.update(
        {
            cons.ECG_MODIFIED_DATE: current_date
        }
    )
    query = {field_name: item_id}
    new_values = { cons.CONS_SET_STR: jsonecg_propertyStr }

    x = ecg_col.update_one(query, new_values)
    return x.modified_count

def update_ecg_file(db, field_name, item_id, list_new_values: ECG):
    x = db.fs.files.update_many(
        {field_name: item_id},
        {cons.CONS_SET_STR: {
            cons.ECG_CHANNEL: list_new_values.channel,
            cons.ECG_MODIFIED_DATE: common.get_current_date()
        }})
    # Check to return the number of files updated
    if x:
        return x.modified_count
    else:
        return 0

def delete_record(ecg_col, field_name, item_id):
    query = {field_name: item_id}
    x = ecg_col.delete_one(query)
    return x.deleted_count

def delete_ecg_file(db,fs, field_name, item_id):
    data = scraper.find_by_single_item(db.fs.files, field_name, item_id)
    for item in data:
        file_id = item[cons.ECG_ID_SHORT]
        fs.delete(file_id)
        print(f'Deleted file_id: {file_id}')
