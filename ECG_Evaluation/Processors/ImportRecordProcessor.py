import streamlit as st
import Controllers.Constants as cons
import Controllers.Common as common
import Scraper as scraper
from Controllers.ECGModel import ECG
import Controllers.Helper as helper
import os
from Controllers.FilesModel import Files
import Views.ImportRecordView as import_record_view
import Controllers.WFDBHelper as wfdb_helper

class ImportRecordProcessor:
    def process_file(self, dir_name):
        file_list=[]
        for root, dirs, files in os.walk(dir_name):
            for file in files:
                file_name= helper.get_file_name(file)
                file_path = os.path.join(dir_name,file)
                file_index = helper.get_file_index(file_name, file_list)
                if isinstance(file_index, int):
                    file_list[file_index].file_name_ext.append(file)
                    file_list[file_index].file_path.append(file_path)
                else:
                    file_list.append(Files(
                        file_name_ext=[file],
                        file_path=[file_path],
                        file_name=file_name
                    ))
        if not file_list:
            st.error('Cannot read source folder!')
            st.stop()
        return file_list

    def render_property(self, ecg_property : ECG):
        # Count number of channels from record
        total_channels = len(ecg_property.sample[0])

        # Check if the unit is None, set [mV, V] as options for the selectbox
        # Otherwise, set the current value to the list for the selectbox
        if ecg_property.unit:
            ecg_property.unit = [ecg_property.unit]
        else:
            ecg_property.unit = [cons.CONS_UNIT_MV, cons.CONS_UNIT_V]

        # Get result after rendering property
        # result = {
        #    cons.ECG_SOURCE: source,
        #    cons.ECG_CHANNEL: channel,
        #    cons.ECG_SAMPLE_RATE: sample_rate,
        #    cons.ECG_TIME: time,
        #    cons.ECG_TOTAL_CHANNELS: total_channels
        #   }
        result = import_record_view.render_property(ecg_property, total_channels)

        # Count number of channels when missing recording metadata
        # User will enter the channel manually (Ex: I;II;III)
        is_channel_from_record = result[cons.ECG_CHANNEL_TEXT]
        channel = result[cons.ECG_CHANNEL]
        
        # Process to get list of channel when user enters manually
        if (not is_channel_from_record):
            channel = common.convert_string_to_list(channel, cons.CONS_SEMICOLON)
            
        # Check input channels vs total channels of source
        # First check is used for channels, which entered manually
        # Second check is used for channels, which came from the record
        if ((not is_channel_from_record and ((channel[0] == '' and total_channels == len(channel)) or (not channel[0] == '' and not total_channels == len(channel)))) or 
            ecg_property.channel and not len(ecg_property.channel) == len(channel)):
            st.error('Input channels must be equal to the total channels of the source!')
            return None
        else:
            return ECG(
                source=result[cons.ECG_SOURCE],
                file_name=ecg_property.file_name,
                channel=channel,
                sample=ecg_property.sample,
                time=result[cons.ECG_TIME],
                sample_rate=result[cons.ECG_SAMPLE_RATE],
                ecg=ecg_property.ecg,
                created_date=ecg_property.created_date,
                modified_date=ecg_property.modified_date,
                unit=result[cons.ECG_UNIT],
                comments=result[cons.ECG_COMMENTS]
            )

    def save_ecg_property(self, db_result, dir_name, list_file_path, list_file_name_ext, file_name, final_ecg_property:ECG):
        db= db_result[cons.DB_NAME]
        ecg_col= db_result[cons.COLLECTION_ECG_NAME]

        # Unify the format to WFDB (Ex: .mat --> .dat)
        new_file_list = self.unify_format(final_ecg_property,dir_name,final_ecg_property.file_name)

        # Check the result
        if new_file_list and len(new_file_list) == 1:
            # Update the new file list based on the new unified format
            ecg_record = new_file_list[0]

            # Update the number of file generation by the new format
            final_ecg_property.ecg = len(ecg_record.file_path)

            # Update 'sample' property by total number of samples instead of data signal before saving ECG property
            # It can cause an error of 'the BSON document too large'
            final_ecg_property.sample = len(final_ecg_property.sample)

            ecg_id = scraper.save_ecg_property(ecg_col, final_ecg_property)
            if ecg_id:
                list_file_id = []
                for index, item in enumerate(ecg_record.file_path):
                    file_name_ext= ecg_record.file_name_ext[index]
                    file_metadata = Files(
                        file_path=item,
                        file_name_ext=file_name_ext,
                        file_name=file_name, 
                        ecg_id=ecg_id
                        )

                    # Save ECG file to MongoDB
                    file_id = scraper.save_ecg_file(db, file_metadata, final_ecg_property)
                    if file_id:
                        list_file_id.append([file_id])
                if len(list_file_id) == final_ecg_property.ecg:
                    st.success('Imported successfully!')

    def unify_format(self, ecg_property:ECG, dir_name, file_name):
        # Unify format with WFDB library and return the new folder path with new files
        path = wfdb_helper.unify_format_wfdb(ecg_property, dir_name, file_name)

        # Process to get the list of files when selecting the folder
        file_list:list[Files] = self.process_file(path)

        return file_list