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

def resampling_data(signals, fs_target, fs):
    # Flatten the array for further processing (Ex: array([[0.2735], [0.287], [0.2925], [0.312]]) --> [0.2735, 0.287,  0.2925, 0.312])
    signals_flatten = signals.flatten()
    # Calculate the ratio between the current and target sample rate
    ratio = fs_target/fs
    # Calculate new length of samples
    new_sample_length = int(signals_flatten.shape[0]*ratio)
    # Calculate time signal (origin x-coordinates)
    time_signal = np.arange(signals_flatten.size) / fs
    # Calculate time signal based on the new length of samples (new x-coordinates)
    time_signal_new =np.linspace(time_signal[0], time_signal[-1], new_sample_length, endpoint=True)
    # Calculate the new signal data by using interpolate method
    ########################
    # Syntax : numpy.interp(x, xp, fp, left = None, right = None, period = None)
    # Parameters :
    # x : [array_like] The x-coordinates at which to evaluate the interpolated values.
    # xp: [1-D sequence of floats] The x-coordinates of the data points, must be increasing if the argument period is not specified.
    #       Otherwise, xp is internally sorted after normalizing the periodic boundaries with xp = xp % period.
    # fp : [1-D sequence of float or complex] The y-coordinates of the data points, same length as xp.
    ########################
    # x = time_signal_new --> new array of calculating the duration based on the length of the samples
    # xp = time_signal --> origin array of duration
    # fp = signals_flatten --> origin array of signal data, which is fattened
    ########################
    resampled_signal = np.interp(time_signal_new, time_signal, signals_flatten)
    return resampled_signal

def visualize_chart(file_name, channel_name, signal, fs, resampled_signal, fs_target):
    time_signal = np.arange(signal.size) / fs
    time_resampled_signal = np.arange(resampled_signal.size) / fs_target

    fig, axs = plt.subplots(2)
    fig.suptitle('File name: {}, ExpTemp channel: {}'.format(file_name, channel_name))
    axs[0].plot(time_signal, signal, color='blue', marker='o')#, label='Sample rate: ' + str(fs) + ' - Number of samples: ' + str(len(signal)))
    axs[0].set_title('Feq: {} - Samples: {}'.format(str(fs),str(len(signal))))
    axs[1].plot(time_resampled_signal, resampled_signal, color='orange', marker='o')#,label='Sample rate: ' + str(fs_target) + ' - Number of samples: ' + str(len(resampled_signal)))
    axs[1].set_title('Feq: {} - Samples: {}'.format(str(fs_target), str(len(resampled_signal))))

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
