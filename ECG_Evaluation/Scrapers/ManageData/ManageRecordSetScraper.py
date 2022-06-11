import Controllers.Common as common
import Controllers.Constants as cons
import Scraper as scraper
from Controllers.RecordSetModel import RecordSet

def find_record_list(my_col, query_data):
    match_query = {
        # Find all data, no condition
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

def update_record_set(record_set_col, field_name, item_id, list_new_values: RecordSet):
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

def delete_record_set(record_set_col, field_name, item_id):
    query = {field_name: item_id}
    x = record_set_col.delete_one(query)
    return x.deleted_count