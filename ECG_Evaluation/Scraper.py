from bson.objectid import ObjectId
import gridfs
import Controllers.ECGModel as ecg_model
import Controllers.Common as common
import Controllers.Constants as cons

def connect_gridfs(my_db):
    return gridfs.GridFS(my_db)

def save_ecg_property(my_col, ecg_property: ecg_model.ECG):
    jsonecg_propertyStr = common.parse_json(ecg_property.__dict__)
    output = my_col.insert_one(jsonecg_propertyStr)
    if output:
        print('ecg_id: ' + str(output))
    return output.inserted_id

def save_ecg_file(my_db, file_path, file_name, ecg_id):
    file_data = open(file_path, "rb")
    data = file_data.read()
    fs = connect_gridfs(my_db)
    result = fs.put(data=data, file_name = file_name)
    output = fs.get(result)
    file_id = output._id
    my_db.fs.files.update({cons.ECG_ID_SHORT: file_id}, {cons.CONS_SET_STR: {cons.ECG_ID: ecg_id}})
    if file_id:
        print('file_id: ' + str(file_id))
        print('file_path: ' + file_path)
        return file_id

def retrieve_ecg_file(my_db, ecg_id):
    # fs = connect_gridfs(my_db)
    data = my_db.fs.files.find({cons.ECG_ID: ObjectId(ecg_id)})
    testid = data[cons.ECG_ID_SHORT]
    print(testid)