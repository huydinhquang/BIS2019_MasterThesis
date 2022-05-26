import streamlit as st
import Controllers.Constants as cons
import os
import numpy as np
import Controllers.Helper as helper

class Processor:
    def __init__(self):
        self.ecg_list = []
        self.ecg = None

    def add(self, ecg):
        self.ecg_list.append(ecg)

    def set(self, ecg):
        self.ecg = ecg

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
        return self.ecg.get_source_property()