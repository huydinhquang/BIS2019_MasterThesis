import streamlit as st
from Controllers.ECGModel import ECG
import wfdb
from datetime import datetime

current_date = datetime.now()

def get_source_property(file_name, dir_name):
    signals, fields = wfdb.rdsamp(dir_name + '/' + file_name)
    fs = fields['fs']
    time = round(len(signals) / fs)
    channels = len(signals[0])
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

def render_property(ecg_property : ECG):
    col1, col2, col3 = st.columns(3)
    with col1:
        source = st.text_input('Source name', 'Test')
        st.text('Total records')
        st.text(str(ecg_property.record))
    with col2:
        options = st.multiselect(
            'Channel(s)',
            ['I', 'II', 'III',
             'aVR', 'aVL', 'aVF',
             'V1', 'V2', 'V3',
             'V4', 'V5', 'V6'])
        st.text('Total channels')
        st.text(str(len(options)))
    with col3:
        sample_rate = st.slider('Sample rate', 0, 10000,
                               ecg_property.sample_rate)
        st.text('Time(s)')
        st.text(str(ecg_property.time))

    return ECG(
        source=source,
        file_name=ecg_property.file_name,
        channel=len(options),
        record=ecg_property.record,
        time=ecg_property.time,
        sample_rate=sample_rate,
        ecg=ecg_property.ecg,
        created_date=ecg_property.created_date,
        modified_date=ecg_property.modified_date
    )