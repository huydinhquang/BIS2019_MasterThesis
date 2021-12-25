import os
from Controllers.FilesModel import Files
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

def write_file(folder_download, item: Files):
    file_name = get_file_name(item.file_name)
    download_location = os.path.join(folder_download, f'{item.ecg_id}{cons.CONS_UNDERSCORE}{file_name}{cons.CONS_UNDERSCORE}{cons.CONS_TEMP_STR}')
    create_folder(download_location)
    file_location = os.path.join(download_location, item.file_name)
    output = open(file_location, 'wb')
    output.write(item.output_data)
    output.close()

#def get_channel_index(channel, item: Files):


def create_folder(path):
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist 
        os.makedirs(path)
        print(f'The new directory {path} is created!')