import os
from Controllers.FilesModel import Files
from Controllers.ECGModel import ECG
import Controllers.Constants as cons
import h5py
import numpy as np

def switch_format_desc(value):
    value = value.lower()
    switcher = {
        1: "WFDB",
        2: "SciPy",
    }
    return switcher.get(value, "Invalid format descriptor")

def get_file_name(file):
    return file.split(".")[0]

def write_file(download_location, file_name, output_data):
    create_folder(download_location)
    file_location = os.path.join(download_location, file_name)
    output = open(file_location, 'wb')
    output.write(output_data)
    output.close()

def get_item_index(name, list_name):
    for index, y in enumerate(list_name):
        if name == y:
            return index

def get_list_index(name, list_name):
    result = []
    for x in name:
        for index, y in enumerate(list_name):
            if x == y:
                result.append(index)
                break
    return result
    # return [index for index, y in enumerate(list_channel) for x in channel if x==y] # Wrong output order if we use this formula

def get_list_existed_channels(channel, list_channel):
    result = []
    for x in channel:
        for y in list_channel:
            if x == y:
                result.append(y)
                break
    return result

def get_file_index(file_name, list_file:list[Files]):
    result = None
    for index, x in enumerate(list_file):
        if x.file_name == file_name:
            result = index
            break
    return result

def create_folder(path):
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist 
        os.makedirs(path)
        print(f'The new directory {path} is created!')

def get_folder_download(ecg: ECG, list_files:list[Files]):
    # Get the first element if it matches the provided ECG Id
    return next(x.folder_download for x in list_files if x.ecg_id == ecg.id)

def create_hdf5(file_path, file_name, list_dataset):
    ### ---------------- Get the shape of the dataset - It is 3D tensor -----------------   ###
    # Height: 1st dimension is the total number of samples (length)         --> shape[2]    ###
    # Width: 2nd dimension is the number of channels                        --> shape[1]    ###
    # Depth: 3rd dimension is the total number of slices from all records   --> shape[0]    ###
    ### ---------------------------------------------------------------------------------   ###
    with h5py.File(f'{file_path}/{file_name}','w') as file:
        for ds in list_dataset:
            dataset_value = ds[cons.CONS_DS_DATA]
            data_shape = np.array(dataset_value).shape
            if len(data_shape) > 2:
                ds_result = file.create_dataset(ds[cons.CONS_DS_NAME], (data_shape[0],data_shape[1],data_shape[2]), dtype='f', data=dataset_value)
            elif len(data_shape) == 2:
                dt = h5py.special_dtype(vlen=bytes)
                ds_result = file.create_dataset(ds[cons.CONS_DS_NAME], (data_shape[0],data_shape[1]), dtype=dt, data=dataset_value)
            else:
                dt = h5py.special_dtype(vlen=bytes)
                ds_result = file.create_dataset(ds[cons.CONS_DS_NAME], (data_shape[0]), dtype=dt, data=dataset_value)
            list_metadata = ds[cons.CONS_DS_METADATA]
            for x in list_metadata:
                ds_result.attrs[x] = list_metadata[x]

def add_value(dict_obj, key, value):
    ''' Adds a key-value pair to the dictionary.
        If the key already exists in the dictionary, 
        it will associate multiple values with that 
        key instead of overwritting its value'''
    if key not in dict_obj:
        dict_obj[key] = value
    elif isinstance(dict_obj[key], list):
        dict_obj[key].append(value)
    else:
        dict_obj[key] = [dict_obj[key], value]