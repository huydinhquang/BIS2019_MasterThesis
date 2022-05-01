from ECGController import ECGController
import streamlit as st
from Controllers.ECGModel import ECG
import wfdb
# import pandas as pd
import Controllers.Constants as cons
# import Controllers.Common as common
import os
from pathlib import Path
import shutil
import numpy as np
import matplotlib.pyplot as plt

# class WFDBHelper:
def get_source_property_with_condition(dir_name, file_name, channel_target):
    # def get_source_property_constraint(self, signal_start, signal_end, channel_target):
    # signals, fields = wfdb.rdsamp(self.dir_name + '/' + self.file_name, sampfrom=signal_start,sampto=signal_end, channels=[channel_target])
    signals, fields = wfdb.rdsamp(os.path.join(dir_name,file_name), channels=channel_target)
    # headers = wfdb.rdheader(dir_name + '/' + file_name)
    fs = fields[cons.SAMPLING_FREQUENCY]
    time = round(len(signals) / fs)
    channels = [item.upper() for item in fields[cons.SINGAL_NAME]] 
    return ECG(
        file_name=file_name,
        channel=channels,
        sample=signals,
        time=time,
        sample_rate=fs
    )

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

# def visualize_chart(self, signals, fs, channels):
#     for channel in range(channels):        
#         #     wfdb.plot_items(signal=signals, fs=fields['fs'], title='Huy Test')
#         #     st.pyplot(signals)
#         signals, fields = wfdb.rdsamp(self.dirname + '/' + self.fileName, channels=[channel])
#         timeArray = np.arange(signals.size) / fs
#         plt.plot(timeArray, signals)
#         plt.xlabel("time in s")
#         plt.ylabel("ECG in mV")
#         st.pyplot(plt)

def resampling_data(signals, fs_target, fs):
    signals_flatten = signals.flatten()
    ratio = fs_target/fs
    # Calculate new length of sample
    new_sample_length = int(signals_flatten.shape[0]*ratio)
    new_samples_singal=np.linspace(signals_flatten[0], signals_flatten[-1], new_sample_length, endpoint=True)
    current_signal_position = np.linspace(signals_flatten[0], signals_flatten[-1], len(signals_flatten), endpoint=True)
    resampled_signal = np.interp(new_samples_singal, current_signal_position, signals_flatten)
    return resampled_signal

def visualize_chart(signals, resampled_signal, fs_target):
        # for channel in range(channels):        
        #     wfdb.plot_items(signal=signals, fs=fields['fs'], title='Huy Test')
        #     st.pyplot(signals)
        

        time = np.arange(signals.size) / fs_target

        # plot1 = plt.figure(1)
        plt.plot(time, signals, color='blue', marker='o')

        # plot2 = plt.figure(2)
        plt.plot(time, resampled_signal, color='green', marker='o')

        # fig1 = plt.figure()
        # fig2 = plt.figure()

        # ax1 = fig1.add_subplot(111)
        # ax2 = fig2.add_subplot(111)

        # ax1.plot(time, signals, color='blue', marker='o')
        # ax2.plot(time, resampled_signal, color='blue', marker='o')

        # ax1.plot(time, signals, color='blue', marker='o')
        # ax1.set(xlabel='time in s', ylabel='ECG in mV')
        # ax2.plot(time, resampled_signal, color='blue', marker='o')
        # ax2.set(xlabel='time in s', ylabel='ECG in mV')

        # plt.plot(time, signals,marker='o')
        # plt.xlabel("time in s")
        # plt.ylabel("ECG in mV")
        plt.show()
        # st.pyplot(plt)
