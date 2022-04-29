from bson.objectid import ObjectId
from pymongo import helpers
import streamlit as st
import wfdb
from datetime import datetime
import pandas as pd
import Controllers.Constants as cons
import Controllers.Common as common
from Controllers.RecordSetModel import RecordSet
from Controllers.ExportingTemplateModel import ExportingTemplate
import Scrapers.ExportDataScraper as export_data_scraper
import Views.DownloadChannel as download_channel
import Scraper as scraper
import Scrapers.RecordSetScraper as record_set_scraper
from Controllers.ECGModel import ECG
import Controllers.Helper as helper
import os
import Controllers.WFDBHelper as wfdb_helper
from Controllers.FilesModel import Files
import numpy as np

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