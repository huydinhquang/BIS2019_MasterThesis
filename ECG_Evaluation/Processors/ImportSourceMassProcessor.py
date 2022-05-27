import streamlit as st
import Controllers.Constants as cons
import Controllers.Common as common
import Controllers.Helper as helper
import Scraper as scraper
from Controllers.ECGModel import ECG
import Controllers.Helper as helper
import os
from Controllers.FilesModel import Files
import numpy as np
import Controllers.WFDBHelper as wfdb_helper

class ImportSourceMassProcessor:
    def save_ecg_property_masss(self, db_result, dir_name, file_list:list[Files], format_desc, list_ecg_attributes):
        # Check source, which must be defined
        source = list_ecg_attributes[cons.ECG_SOURCE]
        if not source:
            st.warning('Source must be defined!')
            return
        
        db= db_result[cons.DB_NAME]
        ecg_col= db_result[cons.COLLECTION_ECG_NAME]

        # Process each record from the folder
        for ecg_record in file_list:
            # Access and read the ECG record property
            ecg_property:ECG = wfdb_helper.read_property(dir_name, ecg_record.file_path, ecg_record.file_name,format_desc.lower())
            # Update 'sample' property by total number of samples instead of data signal before saving ECG property
            # It can cause an error of 'the BSON document too large'
            ecg_property.sample = len(ecg_property.sample)

            # Check if the sample_rate is NOT defined, use the given sample rate from UI
            if not ecg_property.sample_rate:
                fs = list_ecg_attributes[cons.ECG_SAMPLE_RATE]
                ecg_property.sample_rate = fs
                ecg_property.time =  round(ecg_property.sample / fs)

            # Check if the unit is NOT defined, use the given unit from UI
            if not ecg_property.unit:
                ecg_property.unit = list_ecg_attributes[cons.ECG_UNIT]

            # Set values for source and comments from UI to import into DB
            ecg_property.source = source
            ecg_property.comments = list_ecg_attributes[cons.ECG_COMMENTS]

            # Save the ECG property to MongoDB
            ecg_id = scraper.save_ecg_property(ecg_col, ecg_property)
            if ecg_id:
                list_file_id = []
                for index, item in enumerate(ecg_record.file_path):
                    file_path = item
                    file_name_ext= ecg_record.file_name_ext[index]
                    file_metadata = Files(
                        file_path=file_path,
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