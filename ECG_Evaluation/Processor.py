import streamlit as st
from Controllers.ECGModel import ECG
import wfdb
from datetime import date

def GetSourceProperty(fileName, dirName):
    currentDate = date.today()
    signals, fields = wfdb.rdsamp(dirName + '/' + fileName)
    fs = fields['fs']
    time = round(len(signals) / fs)
    chanels = len(signals[0])
    # st.text('Channel(s): ' + str(chanels))
    # st.text('Record(s): ' + str(len(signals)))
    # st.text('Time(s): ' + str(time))
    # st.text('Sample rate: ' + str(fs))
    return ECG(
        source=None,
        file_name=fileName,
        channel=chanels,
        record=len(signals),
        time=time,
        sample_rate=fs,
        ecg=None,
        created_date=currentDate,
        modified_date=currentDate
    )
