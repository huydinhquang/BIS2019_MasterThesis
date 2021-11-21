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

current_date = datetime.now()

if 'select_row' not in st.session_state:
	st.session_state.select_row = False

# def visualizeChart(signals, fs, channels):
#     for channel in range(channels):        
#         #     wfdb.plot_items(signal=signals, fs=fields['fs'], title='Huy Test')
#         #     st.pyplot(signals)
#         signals, fields = wfdb.rdsamp(dirname + '/' + fileName, channels=[channel])
#         timeArray = np.arange(signals.size) / fs
#         plt.plot(timeArray, signals)
#         plt.xlabel("time in s")
#         plt.ylabel("ECG in mV")
#         st.pyplot(plt)

def write_channel(final_ecg_property : ECG, file_name, dir_name):
    list_sub_channel_folder = []
    for idx, channel in enumerate(final_ecg_property.channel):
        # Create folder for each channel
        path = dir_name + '/' + channel
        list_sub_channel_folder.append(path)
        if os.path.exists(path):
            shutil.rmtree(path)
        Path(path).mkdir(parents=True, exist_ok=True)

        # Write channel to the folder
        signals, fields = wfdb.rdsamp(dir_name + '/' + file_name, channels=[idx])
        wfdb.wrsamp(record_name=channel, fs = final_ecg_property.sample_rate, units=['mV'], sig_name=[channel], p_signal=signals, write_dir=path)
    return list_sub_channel_folder

def get_source_property(file_name, dir_name):
    try:
        signals, fields = wfdb.rdsamp(dir_name + '/' + file_name)
        # headers = wfdb.rdheader(dir_name + '/' + file_name)
        fs = fields[cons.SAMPLING_FREQUENCY]
        time = round(len(signals) / fs)
        channels = [item.upper() for item in fields[cons.SINGAL_NAME]] 
        return ECG(
            id=None,
            source=None,
            file_name=file_name,
            channel=channels,
            record=len(signals),
            time=time,
            sample_rate=fs,
            ecg=None,
            created_date=current_date,
            modified_date=current_date
        )
    except ValueError:
        e = RuntimeError('Cannot read source property!')
        st.exception(e)

def render_property(ecg_property : ECG):
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

def load_source_data(my_col, list_channel):
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