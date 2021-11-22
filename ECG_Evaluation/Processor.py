import streamlit as st
from Controllers.ECGModel import ECG
import wfdb
from datetime import datetime
import pandas as pd
import Controllers.Constants as cons
import Controllers.Common as common
import os
from pathlib import Path
import shutil
import numpy as np
import matplotlib.pyplot as plt
import Views.DBImport as db_import
import Views.AnnotationExtractor as ann_extract

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
                dir_list.append([dir_name + '/' + file])
                if not file_name:
                    file_name = file.split(".")[0]
        if not file_list or not dir_list:
            st.error('Cannot read source folder!')
            st.stop()
        return np.concatenate((file_list, dir_list), axis=1), file_name

    def get_source_property(self):
        for e in self.ecg_list:
            return e.get_source_property()

    def render_property(self, ecg_property : ECG):
        source, channel = db_import.render_property(ecg_property)
            
        # Check input channels vs total channels of source
        if not len(ecg_property.channel) == len(channel):
            st.error('Input channels must be equal to the total channels of the source!')
            return None
        else:
            return ECG(
                id=None,
                source=source,
                file_name=ecg_property.file_name,
                channel=channel,
                record=ecg_property.record,
                time=ecg_property.time,
                sample_rate=ecg_property.sample_rate,
                ecg=ecg_property.ecg,
                created_date=ecg_property.created_date,
                modified_date=ecg_property.modified_date
            )

    def load_source_data(self, my_col, list_channel):
        # st.session_state.select_row = True
        count = 0
        list_ecg = []
        query = {cons.ECG_CHANNEL:{"$in":list_channel}}
        for record in my_col.find(query):
            count = count + 1
            list_ecg.append(ECG(
                source=record[cons.ECG_SOURCE],
                file_name=record[cons.ECG_FILE_NAME],
                channel=common.convert_list_to_string(record[cons.ECG_CHANNEL]).upper(),
                record=record[cons.ECG_RECORD],
                time=record[cons.ECG_TIME],
                sample_rate=record[cons.ECG_SAMPLE_RATE],
                ecg=len(record[cons.ECG_ECG]),
                created_date=common.convert_timestamp_to_datetime(record[cons.ECG_CREATED_DATE]),
                modified_date=common.convert_timestamp_to_datetime(record[cons.ECG_MODIFIED_DATE]),
                id=str(record[cons.ECG_ID])
            ))
            
        header_table = [
            cons.HEADER_SOURCE,
            cons.HEADER_FILENAME,
            cons.HEADER_CHANNEL,
            cons.HEADER_RECORD,
            cons.HEADER_TIME,
            cons.HEADER_SAMPLE_RATE,
            cons.HEADER_ECG,
            cons.HEADER_CREATED_DATE,
            cons.HEADER_MODIFIED_DATE,
            cons.HEADER_ID
        ]

        df = pd.DataFrame.from_records([vars(s) for s in list_ecg])
        df.columns = header_table

        st.write('### Full Dataset', df)
        st.info('Total items: ' + str(count))
        selected_indices = st.multiselect('Select rows:', df.index)
        if selected_indices or st.session_state.select_row:
            st.session_state.select_row = True
            # st.session_state.get_select_source = True
            selected_rows = df.loc[selected_indices]
            st.write('### Selected Rows', selected_rows)

            clicked = ann_extract.render_download_section()
            if clicked:
                for item in selected_rows:
                    st.write(item[cons.ECG_ID])



# if 'select_row' not in st.session_state:
# 	st.session_state.select_row = False

