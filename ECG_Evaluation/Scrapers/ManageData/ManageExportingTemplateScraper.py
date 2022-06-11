import Controllers.Common as common
import Controllers.Constants as cons
import Scraper as scraper
from Controllers.ExportingTemplateModel import ExportingTemplate


def update_exp_template(record_set_col, field_name, item_id, list_new_values: ExportingTemplate):
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

    x = record_set_col.update_one(query, new_values)
    return x.modified_count

def delete_exp_template(record_set_col, field_name, item_id):
    query = {field_name: item_id}
    x = record_set_col.delete_one(query)
    return x.deleted_count