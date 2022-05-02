from cProfile import label
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

def visualize_chart(signal, fs, resampled_signal, fs_target):
    time_signal = np.arange(signal.size) / fs
    time_resampled_signal = np.arange(resampled_signal.size) / fs_target

    fig, axs = plt.subplots(2)
    fig.suptitle('Vertically stacked subplots')
    axs[0].plot(time_signal, signal, color='blue', marker='o')#, label='Sample rate: ' + str(fs) + ' - Number of samples: ' + str(len(signal)))
    axs[0].set_title('Feq: ' + str(fs) + ' - Samples: ' + str(len(signal)))
    axs[1].plot(time_resampled_signal, resampled_signal, color='orange', marker='o')#,label='Sample rate: ' + str(fs_target) + ' - Number of samples: ' + str(len(resampled_signal)))
    axs[1].set_title('Feq: ' + str(fs_target) + ' - Samples: ' + str(len(resampled_signal)))

    for ax in axs.flat:
        ax.set(xlabel='time (s)', ylabel='mV')

    # # Legend
    # handels = []
    # labels = []
    
    # for ax in fig.axes:
    #     Handel, Label = ax.get_legend_handles_labels()
    #     handels.extend(Handel)
    #     labels.extend(Label)
        
    # # Hide x labels and tick labels for top plots and y ticks for right plots.
    # for ax in axs.flat:
    #     ax.label_outer()

    # fig.legend(handels, labels, loc = 'upper right')

    # Tight layout
    fig.tight_layout()
    
    st.pyplot(plt)

# def visualize_chart(signals, fs):
    # # for channel in range(channels):        
    # #     wfdb.plot_items(signal=signals, fs=fields['fs'], title='Huy Test')
    # #     st.pyplot(signals)

    # time = np.arange(signals.size) / fs
    # plt.plot(time, signals,marker='o')
    # plt.xlabel("time in s")
    # plt.ylabel("ECG in mV")
    # st.pyplot(plt)
