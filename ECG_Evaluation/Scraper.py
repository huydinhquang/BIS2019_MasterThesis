import gridfs
import Controllers.ECGModel as ecg_model
import Controllers.Common as common

def save_ecg_property(my_col, ecg_property: ecg_model.ECG, list_file_id):
    ecg_property.ecg = list_file_id
    jsonecg_propertyStr = common.parse_json(ecg_property.__dict__)
    output = my_col.insert_one(jsonecg_propertyStr)
    return output.inserted_id

def save_ecg_file(my_db, file_path, file_name):
    file_data = open(file_path, "rb")
    data = file_data.read()
    fs = gridfs.GridFS(my_db)
    result = fs.put(data, file_name = file_name)
    output = fs.get(result)
    file_id = output._id
    if file_id:
        print('file_id: ' + str(file_id))
        print('file_path: ' + file_path)
        return file_id