# import pandas as pd
import streamlit as st
import wfdb
import os
import numpy as np
import matplotlib.pyplot as plt
import Controllers.Constants as cons
import Controllers.Common as common
import Controllers.Helper as helper
from Processor import Processor
from Controllers.ECGModel import ECG
from Controllers.WFDBController import WFDBController
from Controllers.SciPyController import SciPyController

processor = Processor()

# class WFDBHelper:
def read_property(dir_name, file_list, file_name,format_desc):
    # Read record ecg property    
    if format_desc == cons.CONS_WFDB:
        processor.set(WFDBController(dir_name, file_name, file_list))
    elif format_desc == cons.CONS_SCIPY:
        processor.set(SciPyController(dir_name, file_name, file_list))
    return processor.get_record_property()


def get_record_property(dir_name, file_name):
    signals, fields = wfdb.rdsamp(os.path.join(dir_name,file_name))
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

def get_record_property_with_condition(dir_name, file_name, channel_target, sample_from=None, sample_to=None):
    if sample_from is None or sample_to is None:
        signals, fields = wfdb.rdsamp(os.path.join(dir_name,file_name), channels=channel_target)
    else:
        signals, fields = wfdb.rdsamp(os.path.join(dir_name,file_name), sampfrom=sample_from,sampto=sample_to, channels=channel_target)

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

def write_record(final_ecg_property : ECG, path):
    # # Define a temporary folder
    # temp_folder = f'{common.convert_current_time_to_str()}_{file_name}'
    # # Create folder for record
    # path = os.path.join(dir_name,temp_folder)
    # if os.path.exists(path):
    #     shutil.rmtree(path)
    # Path(path).mkdir(parents=True, exist_ok=True)
    
    # Generate list of units by the number of channels
    list_units = [final_ecg_property.unit] * len(final_ecg_property.channel)

    wfdb.wrsamp(record_name=final_ecg_property.file_name,
                fs=final_ecg_property.sample_rate,
                units=list_units,
                sig_name=final_ecg_property.channel,
                p_signal=final_ecg_property.sample,
                write_dir=path,
                comments=[final_ecg_property.comments])

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


def visualize_record(file_name, ecg_property):
    # Get sample rate (Frequency)
    fs = ecg_property.sample_rate

    # Count total number of channels in the record
    number_channels = len(ecg_property.channel)

    # Set default value for columns visualization
    default_value = 1
    if number_channels > 3:
        default_value = 3
    # Number of columns in visualization
    columns = st.number_input('Columns for record visualization', min_value=1, max_value=number_channels, step=1, value=default_value)

    # Number of rows in visualization
    rows = int(np.ceil(number_channels / columns))

    for idx, x in enumerate(ecg_property.channel):
        # Start the subplot must be 1
        index_subplot = idx + 1

        # Extract signal data from list of samles by vertical axis
            # Horizontal = 0 
            # Vertical = 1
        axis = 1
        signal = np.take(ecg_property.sample, [idx], axis)
        time_signal = np.arange(signal.size) / fs

        plt.subplot(rows, columns, index_subplot)
        plt.plot(time_signal, signal)
        plt.title(f'Channel: {x}')
        plt.xlabel='time (s)'
        plt.ylabel='mV'

    plt.suptitle(f'File name: {file_name}, Feq: {str(fs)}')   
    
    # Tight layout
    plt.tight_layout()
    
    st.pyplot(plt)

def visualize_resampled_signal(file_name, channel_name, signal, fs, resampled_signal, fs_target):
    time_signal = np.arange(signal.size) / fs
    time_resampled_signal = np.arange(resampled_signal.size) / fs_target

    fig, axs = plt.subplots(2)
    fig.suptitle('File name: {}, ExpTemp channel: {}'.format(file_name, channel_name))
    axs[0].plot(time_signal, signal, color='blue', marker='x')#, label='Sample rate: ' + str(fs) + ' - Number of samples: ' + str(len(signal)))
    axs[0].set_title('Feq: {} - Samples: {}'.format(str(fs),str(len(signal))))
    axs[1].plot(time_resampled_signal, resampled_signal, color='orange', marker='x')#,label='Sample rate: ' + str(fs_target) + ' - Number of samples: ' + str(len(resampled_signal)))
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

def unify_format_wfdb(ecg_property:ECG, dir_name, file_name):
    # Define a temporary folder
    temp_folder = f'{common.convert_current_time_to_str()}_{file_name}'
    # Create folder for record
    path = os.path.join(dir_name,temp_folder)
    helper.create_folder(path)

    # Write record to the temporary folder
    write_record(ecg_property, path)

    return path