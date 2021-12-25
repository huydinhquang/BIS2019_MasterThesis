from bson.objectid import ObjectId
import gridfs
import Controllers.ECGModel as ecg_model
import Controllers.Common as common
import Controllers.Constants as cons
from Controllers.FilesModel import Files
from Controllers.ECGModel import ECG


def connect_gridfs(my_db):
    return gridfs.GridFS(my_db)


def save_ecg_property(my_col, ecg_property: ecg_model.ECG):
    jsonecg_propertyStr = common.parse_json(ecg_property.__dict__)
    output = my_col.insert_one(jsonecg_propertyStr)
    if output:
        print('ecg_id: ' + str(output))
    return output.inserted_id


def save_ecg_file(my_db, file_path, file_name, ecg_id, final_ecg_property: ECG):
    file_data = open(file_path, "rb")
    data = file_data.read()
    fs = connect_gridfs(my_db)
    result = fs.put(data=data, file_name=file_name)
    output = fs.get(result)
    file_id = output._id
    my_db.fs.files.update({cons.ECG_ID_SHORT: file_id}, {cons.CONS_SET_STR: {
                          cons.ECG_ID: ecg_id, cons.ECG_CHANNEL: final_ecg_property.channel}})
    if file_id:
        print('file_id: ' + str(file_id))
        print('file_path: ' + file_path)
        return file_id


def find_by_query(my_col, query_type, field_name, list_item):
    query = {field_name: {query_type: list_item}}
    return my_col.find(query)


def retrieve_ecg_file(my_db, list_ecg_id:ECG):
    data = find_by_query(
        my_db.fs.files, cons.CONS_QUERYIN_STR, cons.ECG_ID, list_ecg_id.id)
    fs = connect_gridfs(my_db)
    files = []
    for item in data:
        file_name = item[cons.ECG_FILE_NAME]
        file_id = item[cons.FILE_ID_SHORT]
        ecg_id = item[cons.ECG_ID]
        channel = item[cons.ECG_CHANNEL]
        files.append(Files(file_name, fs.get(file_id).read(), ecg_id, channel))
    return files
