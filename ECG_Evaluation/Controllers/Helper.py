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

def get_channel_index(channel, list_channel):
    result = []
    for x in channel:
        for index, y in enumerate(list_channel):
            if x == y:
                result.append(index)
                break
    return result
    # return [index for index, y in enumerate(list_channel) for x in channel if x==y] # Wrong output order if we use this formula

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

def create_hdf5(file_path, file_name, dataset_name, dataset_value):
    ### ---------------- Get the shape of the dataset - It is 3D tensor -----------------   ###
    # Height: 1st dimension is the total number of samples (length)         --> shape[2]    ###
    # Width: 2nd dimension is the number of channels                       --> shape[1]     ###
    # Depth: 3rd dimension is the total number of slices from all records  --> shape[0]     ###
    ### ---------------------------------------------------------------------------------   ###
    data_shape = np.array(dataset_value).shape
    with h5py.File(f'{file_path}/{file_name}','w') as file:
        dset1 = file.create_dataset(dataset_name, (data_shape[0],data_shape[1],data_shape[2]), dtype='f', data=dataset_value)
        dset1.attrs['qhi'] = 'test'