from bson.objectid import ObjectId
import gridfs
import Controllers.Common as common
import Controllers.Constants as cons
from Controllers.FilesModel import Files
from Controllers.ECGModel import ECG


def connect_gridfs(db):
    return gridfs.GridFS(db)


def save_ecg_property(ecg_col, ecg_property: ECG):
    jsonecg_propertyStr = common.parse_json(ecg_property.__dict__)
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
            cons.ECG_ID: file.ecg_id,
            cons.FILE_ECG_FILE_NAME_EXT: file.file_name_ext,
            cons.ECG_CHANNEL: final_ecg_property.channel
        }})
    if file_id:
        print('file_id: ' + str(file_id))
        print('file_path: ' + file.file_path)
        return file_id


def find_by_query(ecg_col, query_type, field_name, list_item):
    query = {field_name: {query_type: list_item}}
    return ecg_col.find(query)


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
    query = [
        {
            cons.CONS_QUERY_MATCH_QUERY: query_data[cons.CONS_QUERY_MATCH_QUERY]
        },
        {
            cons.CONS_QUERY_LOOKUP_QUERY: query_data[cons.CONS_QUERY_LOOKUP_QUERY]
        }]
    return my_col.aggregate(query)


def retrieve_ecg_file(db, list_selected_ecg_id):
    data = find_by_query(
        db.fs.files, cons.CONS_QUERYIN_STR, cons.ECG_ID, list_selected_ecg_id)
    fs = connect_gridfs(db)
    files = []
    for item in data:
        files.append(Files(
            file_name=item[cons.ECG_FILE_NAME],
            file_name_ext=item[cons.FILE_ECG_FILE_NAME_EXT],
            output_data=fs.get(item[cons.FILE_ID_SHORT]).read(),
            ecg_id=item[cons.ECG_ID],
            channel=item[cons.ECG_CHANNEL]))
    return files

def update_item(ecg_col, field_name, item_id, list_new_values: ECG):
    jsonecg_propertyStr = common.parse_json(list_new_values.__dict__)
    query = {field_name: item_id}
    new_values = { cons.CONS_SET_STR: jsonecg_propertyStr }

    x = ecg_col.update_one(query, new_values)
    return x.modified_count