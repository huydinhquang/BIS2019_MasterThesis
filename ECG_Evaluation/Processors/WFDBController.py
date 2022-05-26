from ECGController import ECGController
import streamlit as st
from Controllers.ECGModel import ECG
import wfdb
import Controllers.Constants as cons
import os
from pathlib import Path
import shutil
import numpy as np
import matplotlib.pyplot as plt

class WFDBController(ECGController):
    def __init__(self, dir_name, file_name, file_list):
        super().__init__(dir_name, file_name, file_list)

    def get_source_property(self):
        signals, fields = wfdb.rdsamp(os.path.join(self.dir_name,self.file_name))
        # headers = wfdb.rdheader(dir_name + '/' + file_name)
        fs = fields[cons.SAMPLING_FREQUENCY]
        # Distinct list of Amplitude unit if they have the same value
        list_unit = list(dict.fromkeys(fields[cons.AMPLITUDE_UNIT]))
        # Return the only one value (Ex: mV or V). Otherwise, return 'None' list due to the differece between signals
        unit = None
        if len(list_unit) == 1:
            unit = list_unit[0]
        time = round(len(signals) / fs)
        channels = [item.upper() for item in fields[cons.SINGAL_NAME]] 
        return ECG(
            file_name=self.file_name,
            channel=channels,
            sample=signals,
            unit=unit,
            time=time,
            sample_rate=fs,
            ecg=len(self.file_list), # Total number of related ECG files
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
