import gridfs
import Controllers.Common as common
import Controllers.Constants as cons
from Controllers.FilesModel import Files
from Controllers.ECGModel import ECG


def connect_gridfs(db):
    return gridfs.GridFS(db)


def save_ecg_property(ecg_col, ecg_property: ECG):
    jsonecg_propertyStr = common.parse_json(ecg_property.__dict__)
    # Get current date
    current_date = common.get_current_date()
    # Update Created date and Modified date with the Date Type (This is used to handle the Date type in MongoDB)
    jsonecg_propertyStr.update(
        {
            cons.ECG_CREATED_DATE: current_date,
            cons.ECG_MODIFIED_DATE: current_date
        }
    )
    output = ecg_col.insert_one(jsonecg_propertyStr)
    if output:
        print('ecg_id: ' + str(output))
    return output.inserted_id


def save_ecg_file(db, file: Files, final_ecg_property: ECG):
    file_data = open(file.file_path, "rb")
    data = file_data.read()
    fs = connect_gridfs(db)
    result = fs.put(data=data, file_name=file.file_name)
    output = fs.get(result)
    file_id = output._id
    db.fs.files.update(
        {cons.ECG_ID_SHORT: file_id},
        {cons.CONS_SET_STR: {
            cons.FILE_ECG_ID: file.ecg_id,
            cons.FILE_ECG_FILE_NAME_EXT: file.file_name_ext,
            cons.ECG_CHANNEL: final_ecg_property.channel,
            cons.ECG_MODIFIED_DATE: common.get_current_date()
        }})
    if file_id:
        print('file_id: ' + str(file_id))
        print('file_path: ' + file.file_path)
        return file_id

def find_by_single_item(col, field_name, item):
    query = {field_name: item}
    return col.find(query)

def find_by_query(col, query_type, field_name, list_item):
    query = {field_name: {query_type: list_item}}
    return col.find(query)


def find(col):
    return col.find()


def find_with_aggregate(my_col, query_data):
    # query = [{
    #     "$match": {
    #         '_id':ObjectId('625aa279ced1267d2208e9e2')
    #     },
    #     "$lookup": {
    #         'from': 'ecg', 'localField': 'source', 'foreignField': 'source', 'as': 'ecg'
    #     }
    # }]
    is_match_query = query_data[cons.CONS_QUERY_MATCH_QUERY]
    if is_match_query:
        query = [
            {
                cons.CONS_QUERY_MATCH_QUERY: query_data[cons.CONS_QUERY_MATCH_QUERY]
            },
            {
                cons.CONS_QUERY_LOOKUP_QUERY: query_data[cons.CONS_QUERY_LOOKUP_QUERY]
            }]
    # Find all, and then aggregate
    else:
        query = [
            {
                cons.CONS_QUERY_LOOKUP_QUERY: query_data[cons.CONS_QUERY_LOOKUP_QUERY]
            }]
    return my_col.aggregate(query)
