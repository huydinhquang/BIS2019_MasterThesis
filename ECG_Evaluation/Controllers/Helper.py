import os
from Controllers.FilesModel import Files
from Controllers.ECGModel import ECG
import Controllers.Constants as cons

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
    # return [index for index, y in enumerate(list_channel) for x in channel if x==y] # Wrong order

def create_folder(path):
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist 
        os.makedirs(path)
        print(f'The new directory {path} is created!')