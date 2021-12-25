from bson.objectid import ObjectId
from pymongo import helpers
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
import Controllers.Helper as helper
import Views.DBImport as db_import
import Views.DownloadChannel as download_channel
import Scraper as scraper

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

    def get_source_property(self):
        for e in self.ecg_list:
            return e.get_source_property()
    
    # def get_source_property_constraint(self):
    #     for e in self.ecg_list:
    #         return e.get_source_property_constraint()

    def render_property(self, ecg_property : ECG):
        # Count number of channels
        total_channels = len(ecg_property.sample[0])

        value = db_import.render_property(ecg_property, total_channels)
            
        # Check input channels vs total channels of source
        if (len(value[cons.ECG_CHANNEL]) == 0 or
            (ecg_property.channel and not len(ecg_property.channel) == len(value[cons.ECG_CHANNEL]))):
            st.error('Input channels must be equal to the total channels of the source!')
            return None
        else:
            return ECG(
                id=None,
                source=value[cons.ECG_SOURCE],
                file_name=ecg_property.file_name,
                channel=value[cons.ECG_CHANNEL],
                sample=len(ecg_property.sample),
                time=value[cons.ECG_TIME],
                sample_rate=value[cons.ECG_SAMPLE_RATE],
                ecg=ecg_property.ecg,
                created_date=ecg_property.created_date,
                modified_date=ecg_property.modified_date
            )

    def load_source_data(self, my_db, my_col, list_channel):
        # st.session_state.select_row = True
        count = 0
        list_ecg = []
        data = scraper.find_by_query(my_col, cons.CONS_QUERYIN_STR, cons.ECG_CHANNEL, list_channel)
        for record in data:
            count = count + 1
            list_ecg.append(ECG(
                source=record[cons.ECG_SOURCE],
                file_name=record[cons.ECG_FILE_NAME],
                channel=common.convert_list_to_string(record[cons.ECG_CHANNEL]).upper(),
                sample=record[cons.ECG_SAMPLE],
                time=record[cons.ECG_TIME],
                sample_rate=record[cons.ECG_SAMPLE_RATE],
                ecg=record[cons.ECG_ECG],
                created_date=common.convert_timestamp_to_datetime(record[cons.ECG_CREATED_DATE]),
                modified_date=common.convert_timestamp_to_datetime(record[cons.ECG_MODIFIED_DATE]),
                id=str(record[cons.ECG_ID_SHORT])
            ))
            
        header_table = [
            cons.HEADER_SOURCE,
            cons.HEADER_FILENAME,
            cons.HEADER_CHANNEL,
            cons.HEADER_SAMPLES,
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

            folder_download, clicked_download = download_channel.render_download_section()
            if clicked_download:
                # print(selected_rows.to_markdown()) 
                list_ecg_id = []
                for index, row in selected_rows.iterrows():
                    list_header_channel = common.convert_string_to_list(row[cons.HEADER_CHANNEL])
                    print(list_header_channel)
                    channel_index = helper.get_channel_index(list_header_channel, list_channel)
                    print(channel_index)
                    list_ecg_id.append(
                        ECG(id=ObjectId(row[cons.HEADER_ID], channel=channel_index, file_name=row[cons.HEADER_FILENAME])))
                    # print(value)
                if len(list_ecg_id) > 0:
                    print(list_ecg_id)
                    list_files = scraper.retrieve_ecg_file(my_db, list_ecg_id)
                    for x in list_files:
                        file_name = helper.get_file_name(x.file_name)
                        download_location = os.path.join(folder_download, f'{x.ecg_id}{cons.CONS_UNDERSCORE}{file_name}{cons.CONS_UNDERSCORE}{cons.CONS_TEMP_STR}')
                        helper.write_file(download_location, file_name, x.output_data)
                    for x in list_ecg_id:
                        download_location = os.path.join(folder_download, f'{x.id}{cons.CONS_UNDERSCORE}{x.file_name}')
                        helper.create_folder(download_location, x)
                    st.success('Download completed!')


    def visualize_chart(self, signals, fs_target, fs):
        # for channel in range(channels):        
        #     wfdb.plot_items(signal=signals, fs=fields['fs'], title='Huy Test')
        #     st.pyplot(signals)
        signals = signals.flatten()
        ratio = fs_target/fs
        # calculate new length of sample
        new_sample_length = int(signals.shape[0]*ratio)
        new_samples_singal=np.linspace(signals[0], signals[-1], new_sample_length, endpoint=False)
        current_signal_position = np.linspace(signals[0], signals[-1], len(signals), endpoint=False)
        resampled_signal = np.interp(new_samples_singal, current_signal_position, signals)
        time = np.arange(resampled_signal.size) / fs_target
        plt.plot(time, resampled_signal,marker='o')
        plt.xlabel("time in s")
        plt.ylabel("ECG in mV")
        st.pyplot(plt)

    def write_channel(self, download_location, ecg_property : ECG):
        # Write channel to the folder
        folder_temp = f'{download_location}{cons.CONS_UNDERSCORE}{cons.CONS_TEMP_STR}'
        signals, fields = wfdb.rdsamp(folder_temp, channels=ecg_property.channel)
        wfdb.wrsamp(record_name=ecg_property.file_name, fs=ecg_property.sample_rate, units=[
                    'mV'], sig_name=ecg_property.channel, p_signal=signals, write_dir=download_location)
