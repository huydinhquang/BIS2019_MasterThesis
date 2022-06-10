import Controllers.Common as common
import Controllers.Constants as cons
from Controllers.ECGModel import ECG


def update_item(ecg_col, field_name, item_id, list_new_values: ECG):
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