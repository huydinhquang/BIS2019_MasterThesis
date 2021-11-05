import streamlit as st
from Controllers.ECGModel import ECG
import wfdb
from datetime import datetime
import pandas as pd
import Controllers.Constants as cons
import json
import Controllers.Common as common
from bson.json_util import loads, dumps

SINGAL_NAME = 'sig_name'
SAMPLING_FREQUENCY = 'fs'
current_date = datetime.now()

def get_source_property(file_name, dir_name):
    try:
        signals, fields = wfdb.rdsamp(dir_name + '/' + file_name)
        # headers = wfdb.rdheader(dir_name + '/' + file_name)
        fs = fields[SAMPLING_FREQUENCY]
        time = round(len(signals) / fs)
        channels = fields[SINGAL_NAME]
        return ECG(
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
        st.error('Cannot read source property!')

def render_property(ecg_property : ECG):
    col1, col2, col3 = st.columns(3)
    with col1:
        source = st.text_input('Source name', 'Test')
        st.text('Total records')
        st.text(str(ecg_property.record))
    with col2:
        channel = st.multiselect('Channel(s)',ecg_property.channel,ecg_property.channel)
        st.text('Total channels')
        st.text(str(len(ecg_property.channel)))
    with col3:
        sample_rate = st.slider('Sample rate', 0, 10000,
                               ecg_property.sample_rate)
        st.text('Time(s)')
        st.text(str(ecg_property.time))
    
    # Check input channels vs total channels of source
    if not len(ecg_property.channel) == len(channel):
        st.error('Input channels  must be equal to the total channels of the source!')
        return None
    else:
        return ECG(
            source=source,
            file_name=ecg_property.file_name,
            channel=channel,
            record=ecg_property.record,
            time=ecg_property.time,
            sample_rate=sample_rate,
            ecg=ecg_property.ecg,
            created_date=ecg_property.created_date,
            modified_date=ecg_property.modified_date
        )

def count_ecg_file(value):
    return len(value)

def load_source_data(my_col, list_channel):
    st.write(list_channel)
    count = 0
    list_ecg = []
    for record in my_col.find():
        count = count + 1
        # list_ecg.append(record)
        list_ecg.append(ECG(
            source=record[cons.ECG_SOURCE],
            file_name=record[cons.ECG_FILE_NAME],
            channel=record[cons.ECG_CHANNEL],
            record=record[cons.ECG_RECORD],
            time=record[cons.ECG_TIME],
            sample_rate=record[cons.ECG_SAMPLE_RATE],
            ecg=count_ecg_file(record[cons.ECG_SOURCE]),
            created_date=record[cons.ECG_CREATED_DATE],
            modified_date=record[cons.ECG_MODIFIED_DATE]
        ))
        
        # json_record = json.dumps(record, default=common.my_handler)
        # list_ecg.append(json_record)
        # st.write(json_record)
    
    df = pd.DataFrame.from_records([vars(s) for s in list_ecg])

    # df = pd.DataFrame (list_ecg, columns = ['List ECG'])
    st.write(df)
    # df = pd.DataFrame()
    # for key, df2 in list_ecg:
    #     df2['index'] = key
    #     df = df.append(df2, ignore_index=True)

    # st.write(count)
    # st.write(list_ecg)
    # st.title("dumps")
    # json_record = json.dumps(list_ecg, default=common.my_handler)
    # st.write(json_record)

    # st.title("loads")
    # record2 = loads(json_record)
    # st.write(record2)
    # # a = json.dumps(record, default=common.my_handler)

    # # Load some example data.
    # # DATA_URL = "http://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz"
    # # data = st.cache(pd.read_json)(my_col.find(), nrows=1000)
    # # data = pd.read_json(list_ecg)
    # # df = pd.DataFrame.from_dict(pd.json_normalize(my_col.find()), orient='columns')
    # # record2 = loads(list_ecg)
    # df = pd.json_normalize(record2)

    # st.write(df)
    # # Select some rows using st.multiselect. This will break down when you have >1000 rows.
    st.write('### Full Dataset', df)
    selected_indices = st.multiselect('Select rows:', df.index)
    selected_rows = df.loc[selected_indices]
    st.write('### Selected Rows', selected_rows)