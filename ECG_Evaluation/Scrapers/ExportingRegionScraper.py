import Controllers.Common as common
import Controllers.Constants as cons
from Controllers.ExportingRegionModel import ExportingRegion
import Scraper as scraper
from Controllers.RecordSetModel import RecordSet

def find_record_list(my_col, query_data):
    item_id =  query_data[cons.CONS_ID_SHORT]
    # Check ID, if no ID is defined, it will search all
    if item_id:
        match_query = {
            cons.CONS_ID_SHORT: item_id
        }
    else:
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

def add_exporting_region(exporting_region_col, values:ExportingRegion):
    current_date = common.get_current_date()
    new_exporting_region_json = {
        cons.CONS_EXPORTING_REGION_RECORD_SET_ID: values.record_set_id,
        cons.FILE_ECG_ID: values.ecg_id,
        cons.CONS_EXPORTING_REGION_START_TIME: values.start_time,
        cons.CONS_EXPORTING_REGION_END_TIME: values.end_time,
        cons.CONS_EXPORTING_REGION_SAMPLE_FROM: values.sample_from,
        cons.CONS_EXPORTING_REGION_SAMPLE_TO: values.sample_to,
        cons.CONS_CREATED_DATE: current_date, 
        cons.CONS_MODIFIED_DATE: current_date
    }
    output = exporting_region_col.insert_one(new_exporting_region_json)
    if output:
        print('exporting_region_id: ' + str(output))
    return output.inserted_id


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