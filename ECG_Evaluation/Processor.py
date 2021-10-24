import streamlit as st
import Controllers.ECGModel as ecgModel

def GetSourceProperty(filePath):
    # ecgData = { "Source": "MIT", "FileName" : "100", "Channel": 2, "Record": 11520000, "Time": 1800, "Sample rate": 500, "ECG" : ['', id]}
    ecg = ecgModel.ECG
    ecg.Source = "MIT"
    ecg.FileName = "100"
    ecg.Channel = 2
    ecg.Record = 11520000
    ecg.Time = 1800
    ecg.SampleRate = 500
    return ecg
    