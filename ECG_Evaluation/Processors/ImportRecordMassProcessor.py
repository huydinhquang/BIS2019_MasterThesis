import streamlit as st
import Controllers.Constants as cons
import Controllers.Common as common
import Controllers.WFDBHelper as wfdb_helper
import Scraper as scraper
from Controllers.ECGModel import ECG
from Controllers.FilesModel import Files
from Processors.ImportRecordProcessor import ImportRecordProcessor

import_record_processor = ImportRecordProcessor()

class ImportRecordMassProcessor:
    def unify_format(self, ecg_property:ECG, dir_name, file_name):
        # Unify format with WFDB library and return the new folder path with new files
        path = wfdb_helper.unify_format_wfdb(ecg_property, dir_name, file_name)

        # Process to get the list of files when selecting the folder
        file_list:list[Files] = import_record_processor.process_file(path)

        return file_list

    def save_ecg_property_mass(self, db_result, dir_name, file_list:list[Files], format_desc, list_ecg_attributes):
        # Check source, which must be defined
        source = list_ecg_attributes[cons.ECG_SOURCE]
        if not source:
            st.warning('Source must be defined!')
            st.stop()
        
        db= db_result[cons.DB_NAME]
        ecg_col= db_result[cons.COLLECTION_ECG_NAME]

        # Process each record from the folder
        for ecg_record in file_list:
            # Access and read the ECG record property
            ecg_property:ECG = wfdb_helper.read_property(dir_name, ecg_record.file_path, ecg_record.file_name,format_desc.lower())
            
            # Set values for source and comments from UI to import into DB
            ecg_property.source = source
            ecg_property.comments = list_ecg_attributes[cons.ECG_COMMENTS]

            # Check if the unit is NOT defined, use the given unit from UI
            if not ecg_property.unit:
                ecg_property.unit = list_ecg_attributes[cons.ECG_UNIT]

            # Check if the channel is NOT defined, use the given channel from UI
            if not ecg_property.channel:
                # Retrieve input value of channel from UI
                channel_input = list_ecg_attributes[cons.ECG_CHANNEL]
                # Stop if there is no defined value
                if not channel_input:
                    st.warning('Channel(s) must be defined!')
                    st.stop()
                else:
                    ecg_property.channel = common.convert_string_to_list(list_ecg_attributes[cons.ECG_CHANNEL], cons.CONS_SEMICOLON)
                    # Check if the number of channels from record with the number of defined channels from UI
                    number_channel_input = len(ecg_property.channel)
                    number_channel_record = ecg_property.sample.shape[1]
                    if not number_channel_input == number_channel_record:
                        st.warning('Number of channel(s) from \'{0}\' record: {1} does not equal number of channel(s) from the input: {2}'.format(ecg_record.file_name, number_channel_record, number_channel_input))
                        st.stop()

            # Count length of the samples
            length_samples = len(ecg_property.sample)

            # Check if the sample_rate is NOT defined, use the given sample rate from UI
            if not ecg_property.sample_rate:
                fs = list_ecg_attributes[cons.ECG_SAMPLE_RATE]
                ecg_property.sample_rate = fs
                ecg_property.time = int(round(length_samples / fs))

            # Unify the format to WFDB (Ex: .mat --> .dat)
            new_file_list = self.unify_format(ecg_property,dir_name,ecg_record.file_name)
            # Check the result
            if new_file_list and len(new_file_list) == 1:
                # Update the new file list based on the new unified format
                ecg_record = new_file_list[0]

                # Update the number of file generation by the new format
                ecg_property.ecg = len(ecg_record.file_path)
            else:
                st.error(f'Cannot unify the format for source name: {ecg_record.file_name}')
                continue

            # Update 'sample' property by total number of samples instead of data signal before saving ECG property
            # It can cause an error of 'the BSON document too large'
            ecg_property.sample = length_samples

            # Save the ECG property to MongoDB
            ecg_id = scraper.save_ecg_property(ecg_col, ecg_property)
            if ecg_id:
                list_file_id = []
                for index, item in enumerate(ecg_record.file_path):
                    file_name_ext= ecg_record.file_name_ext[index]
                    file_metadata = Files(
                        file_path=item,
                        file_name_ext=file_name_ext,
                        file_name=ecg_record.file_name, 
                        ecg_id=ecg_id
                        )

                    # Save ECG files to MongoDB
                    file_id = scraper.save_ecg_file(db, file_metadata, ecg_property)
                    if file_id:
                        list_file_id.append([file_id])
                if len(list_file_id) == ecg_property.ecg:
                    st.success(f'{ecg_record.file_name}: Imported successfully!')