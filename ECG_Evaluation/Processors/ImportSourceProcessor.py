import streamlit as st
import Controllers.Constants as cons
import Controllers.Common as common
import Scraper as scraper
from Controllers.ECGModel import ECG
import Controllers.Helper as helper
import os
from Controllers.FilesModel import Files
import numpy as np
import Views.ImportSourceView as import_source_view

class ImportSourceProcessor:
    def process_file(self, dir_name):
        file_list=[]
        dir_list=[]
        file_name=None
        for root, dirs, files in os.walk(dir_name):
            for file in files:
                file_list.append([
                    {cons.CONS_FILE_LIST:file}
                    ])
                dir_list.append([
                    {cons.CONS_DIR_LIST:os.path.join(dir_name,file)}
                    ])
                if not file_name:
                    file_name = helper.get_file_name(file)
        if not file_list or not dir_list:
            st.error('Cannot read source folder!')
            st.stop()
        return np.concatenate((file_list, dir_list), axis=1), file_name

    def render_property(self, ecg_property : ECG):
        # Count number of channels from source
        total_channels = len(ecg_property.sample[0])

        # Get result after rendering property
        # result = {
        #    cons.ECG_SOURCE: source,
        #    cons.ECG_CHANNEL: channel,
        #    cons.ECG_SAMPLE_RATE: sample_rate,
        #    cons.ECG_TIME: time,
        #    cons.ECG_TOTAL_CHANNELS: total_channels
        #   }
        result = import_source_view.render_property(ecg_property, total_channels)

        # Check if the unit is undefined
        unit = result[cons.ECG_UNIT]
        if unit == cons.CONS_UNDEFINED:
            return None

        # Count number of channels when missing recording metadata
        # User will enter the channel manually (Ex: I;II;III)
        is_channel_from_source = result[cons.ECG_CHANNEL_TEXT]
        channel = result[cons.ECG_CHANNEL]
        
        # Process to get list of channel when user enters manually
        if (not is_channel_from_source):
            channel = common.convert_string_to_list(channel, cons.CONS_SEMICOLON)
            
        # Check input channels vs total channels of source
        # First check is used for channels, which entered manually
        # Second check is used for channels, which came from the source
        if ((not is_channel_from_source and ((channel[0] == '' and total_channels == len(channel)) or (not channel[0] == '' and not total_channels == len(channel)))) or 
            ecg_property.channel and not len(ecg_property.channel) == len(channel)):
            st.error('Input channels must be equal to the total channels of the source!')
            return None
        else:
            return ECG(
                source=result[cons.ECG_SOURCE],
                file_name=ecg_property.file_name,
                channel=channel,
                sample=len(ecg_property.sample),
                time=result[cons.ECG_TIME],
                sample_rate=result[cons.ECG_SAMPLE_RATE],
                ecg=ecg_property.ecg,
                created_date=ecg_property.created_date,
                modified_date=ecg_property.modified_date,
                unit=ecg_property.unit,
                comments=result[cons.ECG_COMMENTS]
            )

    def save_ecg_property(self, db_result, file_list, file_name, final_ecg_property):
        db= db_result[cons.DB_NAME]
        ecg_col= db_result[cons.COLLECTION_ECG_NAME]

        ecg_id = scraper.save_ecg_property(ecg_col, final_ecg_property)
        if ecg_id:
            list_file_id = []
            for item in file_list:
                file_metadata = Files(
                    file_path=item[1][cons.CONS_DIR_LIST],
                    file_name_ext=item[0][cons.CONS_FILE_LIST],
                    file_name=file_name, 
                    ecg_id=ecg_id
                    )

                # Save ECG file to MongoDB
                file_id = scraper.save_ecg_file(db, file_metadata, final_ecg_property)
                if file_id:
                    list_file_id.append([file_id])
            if len(list_file_id) == final_ecg_property.ecg:
                st.success('Imported successfully!')