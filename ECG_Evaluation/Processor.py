import streamlit as st
import Controllers.Constants as cons
import os
import numpy as np
import Controllers.Helper as helper

class Processor:
    def __init__(self):
        self.ecg_list = []

    def add(self, ecg):
        self.ecg_list.append(ecg)

    def print(self):
        for e in self.ecg_list:
            print(f"{e.full_name} \t ${e.get_source_property()}")
    
    def process_file(self, dir_name):
        file_list=[]
        dir_list=[]
        file_name=None
        for root, dirs, files in os.walk(dir_name):
            for file in files:
                # file_name=os.path.join(root, file)
                file_list.append([file])
                dir_list.append([os.path.join(dir_name,file)])
                if not file_name:
                    file_name = helper.get_file_name(file)
        if not file_list or not dir_list:
            st.error('Cannot read source folder!')
            st.stop()
        return np.concatenate((file_list, dir_list), axis=1), file_name

    def process_folder(self, dir_name):
        file_list = [ name for name in os.listdir(dir_name) if os.path.isdir(os.path.join(dir_name, name)) and cons.CONS_TEMP_STR not in name]
        return file_list

    def get_source_property(self):
        for e in self.ecg_list:
            return e.get_source_property()
    
    # def write_channel(self, download_location, list_channel, ecg_property : ECG):
    #         # Extract only selected channels to the folder
    #         # Retrieve the folder temp, which has all original ECG files
    #         folder_temp = f'{download_location}{cons.CONS_UNDERSCORE}{cons.CONS_TEMP_STR}'
    #         # Build the file name with folder path to let WFDB library read the ECG signals
    #         file_name = os.path.join(folder_temp, ecg_property.file_name)
    #         signals, fields = wfdb.rdsamp(file_name, channels=ecg_property.channel)
    #         # Write new ECG files with only selected channels
    #         wfdb.wrsamp(record_name=ecg_property.file_name, fs=ecg_property.sample_rate, units=[
    #                     'mV'], sig_name=list_channel, p_signal=signals, write_dir=download_location)

