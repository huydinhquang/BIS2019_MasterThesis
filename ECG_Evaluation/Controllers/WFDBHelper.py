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

class WFDBHelper:
    def get_source_property_with_condition(self, channel_target):
        # def get_source_property_constraint(self, signal_start, signal_end, channel_target):
        # signals, fields = wfdb.rdsamp(self.dir_name + '/' + self.file_name, sampfrom=signal_start,sampto=signal_end, channels=[channel_target])
        signals, fields = wfdb.rdsamp(os.path.join(self.dir_name,self.file_name), channels=[channel_target])
        # headers = wfdb.rdheader(dir_name + '/' + file_name)
        fs = fields[cons.SAMPLING_FREQUENCY]
        time = round(len(signals) / fs)
        channels = [item.upper() for item in fields[cons.SINGAL_NAME]] 
        return ECG(
            file_name=self.file_name,
            channel=channels,
            sample=signals,
            time=time,
            sample_rate=fs,
            ecg=self.file_list.shape[0], # Total number of ECG files
            created_date=self.current_date,
            modified_date=self.current_date
        )

    def write_channel(self, final_ecg_property : ECG, file_name, dir_name):
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

    def visualize_chart(self, signals, fs, channels):
        for channel in range(channels):        
            #     wfdb.plot_items(signal=signals, fs=fields['fs'], title='Huy Test')
            #     st.pyplot(signals)
            signals, fields = wfdb.rdsamp(self.dirname + '/' + self.fileName, channels=[channel])
            timeArray = np.arange(signals.size) / fs
            plt.plot(timeArray, signals)
            plt.xlabel("time in s")
            plt.ylabel("ECG in mV")
            st.pyplot(plt)