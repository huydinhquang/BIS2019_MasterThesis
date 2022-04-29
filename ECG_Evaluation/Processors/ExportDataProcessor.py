from msilib.schema import File
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
from Controllers.FilesModel import Files
import Controllers.Helper as helper
import os
import Controllers.WFDBHelper as wfdb_helper


class ExportDataProcessor:
    def load_channel_list_from_record_set(self, ecg_col, record_set_col, record_set_id):
        query_data = {
            cons.CONS_QUERY_FROM : ecg_col.name,
            cons.CONS_QUERY_LOCALFIELD: cons.ECG_SOURCE,
            cons.CONS_QUERY_FOREIGNFIELD: cons.CONS_ID_SHORT,
            cons.CONS_QUERY_AS: ecg_col.name,
            cons.CONS_ID_SHORT: record_set_id
        }
        result = export_data_scraper.find_channel_list(record_set_col, query_data)
        return result
    
    def load_record_set_data(self, record_set_col):
        # st.session_state.select_row = True
        count = 0
        list_record_set = []
        # data = scraper.find_by_query(my_main_col, cons.CONS_QUERYREGEX_STR, cons.ECG_SOURCE, source_name)
        record_set_data = scraper.find(record_set_col)
        for record in record_set_data:
            count = count + 1
            list_record_set.append(RecordSet(
                record_set_name=record[cons.CONS_RECORD_SET_NAME],
                created_date=common.convert_time_to_datetime(record[cons.CONS_CREATED_DATE]),
                modified_date=common.convert_time_to_datetime(record[cons.CONS_MODIFIED_DATE]),
                id=str(record[cons.ECG_ID_SHORT]),
                # source=record[cons.ECG_SOURCE]
            ))
            
        header_table = [
            cons.HEADER_RECORD_SET,
            cons.HEADER_CREATED_DATE,
            cons.HEADER_MODIFIED_DATE,
            cons.HEADER_ID,
            cons.HEADER_SOURCE
        ]

        df = pd.DataFrame.from_records([vars(s) for s in list_record_set])
        df.columns = header_table

        return df, count

        #     record_set_name, region_start, region_end, create_clicked = download_channel.record_set()
        #     if create_clicked:
        #         list_selected_ecg = []
        #         for index, row in selected_rows.iterrows():
        #             list_selected_ecg.append(ObjectId(row[cons.HEADER_ID]))
        #         if len(list_selected_ecg) > 0:
        #             record_set_id = record_set_scraper.add_record_set(record_set_col, record_set_name, list_selected_ecg)
        #             return record_set_id

    def load_exp_tem_data(self, exp_tem_col):
        # st.session_state.select_row = True
        count = 0
        list_exp_tem_set = []
        # data = scraper.find_by_query(my_main_col, cons.CONS_QUERYREGEX_STR, cons.ECG_SOURCE, source_name)
        record_set_data = scraper.find(exp_tem_col)
        for record in record_set_data:
            count = count + 1
            list_exp_tem_set.append(ExportingTemplate(
                exporting_template_name=record[cons.CONS_EXPORTING_TEMPLATE_NAME],
                channel=common.convert_list_to_string(record[cons.CONS_CHANNEL]),
                target_sample_rate=str(record[cons.CONS_TARGET_SAMPLE_RATE]),
                duration=str(record[cons.CONS_DURATION]),
                created_date=common.convert_time_to_datetime(record[cons.CONS_CREATED_DATE]),
                modified_date=common.convert_time_to_datetime(record[cons.CONS_MODIFIED_DATE]),
                id=str(record[cons.ECG_ID_SHORT])
            ))
            
        header_table = [
            cons.HEADER_EXP_TEM,
            cons.HEADER_CHANNEL,
            cons.HEADER_TARGET_SAMPLE_RATE,
            cons.HEADER_DURATION,
            cons.HEADER_CREATED_DATE,
            cons.HEADER_MODIFIED_DATE,
            cons.HEADER_ID
        ]

        df = pd.DataFrame.from_records([vars(s) for s in list_exp_tem_set])
        df.columns = header_table

        return df, count

    def load_data(self, db_result):
        ecg_col= db_result[cons.COLLECTION_ECG_NAME]
        record_set_col= db_result[cons.COLLECTION_RECORD_SET_NAME]
        exp_tem_col=db_result[cons.COLLECTION_TEMPLATE_EXPORTATION_NAME]

        # Load full dataset of RecordSet
        df_record_set, count_record_set = self.load_record_set_data(record_set_col)
        st.write('### Full RecordSet', df_record_set)
        st.info('Total items: ' + str(count_record_set))

        record_set_selected_indices = st.selectbox('Select rows:', df_record_set.index)
        record_set_selected_rows = df_record_set.loc[record_set_selected_indices]
        st.write('### Selected Rows', record_set_selected_rows)
            
        # Load full dataset of Exporting Template
        df_exp_tem, count_exp_tem = self.load_exp_tem_data(exp_tem_col)
        st.write('### Full Exporting Template', df_exp_tem)
        st.info('Total items: ' + str(count_exp_tem))
        
        exp_tem_selected_indices = st.selectbox('Select rows:', df_exp_tem.index)
        exp_tem_selected_rows = df_exp_tem.loc[exp_tem_selected_indices]
        st.write('### Selected Rows', exp_tem_selected_rows)

        # Add a 'Generate channel' button
        generate_clicked = st.button('Generate channel')

        if generate_clicked or st.session_state.generate_channel:
            st.session_state.generate_channel = True
            
            # Get RecordSet Id to find related ECG with channels
            record_set_id=ObjectId(record_set_selected_rows[cons.HEADER_ID])
            
            # Query to get list of ECG channels based on RecordSet Id
            result = self.load_channel_list_from_record_set(ecg_col, record_set_col, record_set_id)
            
            # Nested For Loop
            # Loop of RecordSet because it is a result --> Loop of RecordSet-ecg (here is ecg record) --> Get list of channels
            # Ex: 1 record set has many ecg records, and each ecg record has a collection of channels
            # Get more data with Record Id and file name
            ecg_data = [
                ECG(id=y[cons.ECG_ID_SHORT],
                    file_name=y[cons.ECG_FILE_NAME],
                    channel=y[cons.ECG_CHANNEL])
                for x in result for y in x[ecg_col.name]
            ]

            # Get text of channels based on selected exporting template
            list_channels_str = 'Channel ' + exp_tem_selected_rows[cons.HEADER_CHANNEL]
            
            with st.form("extract_data_form"):
                # Widgets will be genrated by the number of ECG records
                # This is used for mapping channel between ECG record and Exporting template
                for x in ecg_data:
                    st.write(list_channels_str + ' from selected exporting template')
                    st.multiselect('Record: ' + x.file_name, x.channel, key=str(x.id))

                folder_download = st.text_input(label='Downloadable folder:', value="C:/Users/HuyDQ/OneDrive/HuyDQ/OneDrive/MasterThesis/Thesis/DB/Download")

                # Every form must have a submit button.
                extract_clicked = st.form_submit_button("Extract data")
                if extract_clicked:
                    self.extract_data(db_result,ecg_data, folder_download)

    def extract_data(self,db_result, ecg_data:list[ECG], folder_download):
        db= db_result[cons.DB_NAME]
        # Loop record in selected RecordSet
        for x in ecg_data:
            selected_channel = st.session_state[x.id]
            channel_index = helper.get_channel_index(selected_channel, x.channel)
            x.channel_index=channel_index

        list_selected_ecg_id = [x.id for x in ecg_data]

        # Search by list of ECG Id to retrieve ECG files
        list_files:list[Files] = scraper.retrieve_ecg_file(db, list_selected_ecg_id)

        # Download and store the ECG files from MongoDB to local
        # Create a folder for each file name to store all related ECG files (Ex: *.dat, *.hea, *.xyz)
        for x in list_files:
            # file_name = helper.get_file_name(x.file_name)
            download_location = os.path.join(folder_download, f'{x.ecg_id}{cons.CONS_UNDERSCORE}{x.file_name}{cons.CONS_UNDERSCORE}{cons.CONS_TEMP_STR}')
            helper.write_file(download_location, x.file_name_ext, x.output_data)
            x.folder_download = download_location

        for x in ecg_data:
            download_location = helper.get_folder_download(x, list_files)
            ecg_property = wfdb_helper.get_source_property_with_condition(download_location, x.file_name, x.channel_index)
            st.write('test')
            
    #     for x in ecg_data:
    #         # print(x.file_name)
    #         # print(x.id)
    #         download_location = os.path.join(folder_download, f'{x.id}{cons.CONS_UNDERSCORE}{x.file_name}')
    #         helper.create_folder(download_location)
    #         self.write_channel(download_location, x.channel_index, x)
    #     st.success('Download completed!')

    # def write_channel(self, download_location, list_channel, ecg_property : ECG):
    #         # Extract only selected channels to the folder
    #         # Retrieve the folder temp, which has all original ECG files
    #         folder_temp = f'{download_location}{cons.CONS_UNDERSCORE}{cons.CONS_TEMP_STR}'
    #         # Build the file name with folder path to let WFDB library read the ECG signals
    #         file_name = os.path.join(folder_temp, ecg_property.file_name)
    #         signals, fields = wfdb.rdsamp(file_name, channels=ecg_property.channel)
    #         # Write new ECG files with only selected channels
    #         wfdb.wrsamp(record_name=ecg_property.file_name, fs=ecg_property.sample_rate, units=[
    #                     'mV'], sig_name=list_channel, p_signal=signals, write_dir=download_location)