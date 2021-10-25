import streamlit as st
from Controllers.ECGModel import ECG

def GetSourceProperty(filePath):
    return ECG(source="MIT", file_name="100", channel=2, record=11520000, time=1800, sample_rate=500, ecg=None)
    # ecg = ecgModel.ECG
    # ecg.Source = "MIT"
    # ecg.FileName = "100"
    # ecg.Channel = 2
    # ecg.Record = 11520000
    # ecg.Time = 1800
    # ecg.SampleRate = 500
    # return ecg
    