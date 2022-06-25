from bson.objectid import ObjectId
import numpy as np
import streamlit as st
from traitlets import default
from Controllers.RecordSetModel import RecordSet
import pandas as pd
import Controllers.Constants as cons
import Controllers.Common as common
from Controllers.ExportingRegionModel import ExportingRegion
import Scrapers.ExportingRegionScraper as exporting_region_scraper
from Controllers.ECGModel import ECG

CONS_ECG_DESC_STR = 'ecg_desc_str'
CONS_ECG_LIST = 'ecg_list'

class ExportingRegionProcessor:
    def get_first_record_set_from_list(self, list_item:list[RecordSet], field_value):
        return next(x for x in list_item if x.id == field_value)

    def load_record_list_from_record_set(self, ecg_col, record_set_col, record_set_id = None):
        query_data = {
            cons.CONS_QUERY_FROM : ecg_col.name,
            cons.CONS_QUERY_LOCALFIELD: cons.ECG_SOURCE,
            cons.CONS_QUERY_FOREIGNFIELD: cons.CONS_ID_SHORT,
            cons.CONS_QUERY_AS: ecg_col.name,
            cons.CONS_ID_SHORT: record_set_id
        }
        result = exporting_region_scraper.find_record_list(record_set_col, query_data)
        return result

    def retrieve_ecg_data(self, ecg:list[ECG]):
        ecg_list = []
        for x in ecg:
            ecg_data = {
                CONS_ECG_DESC_STR: f'Source: {x[cons.ECG_SOURCE]} - File name: {x[cons.ECG_FILE_NAME]}'
            }
            ecg_list.append(ecg_data)
        ecg_desc_str = f'{cons.CONS_SEMICOLON} '.join([x[CONS_ECG_DESC_STR] for x in ecg_list])
        return {
                CONS_ECG_DESC_STR: ecg_desc_str,
                CONS_ECG_LIST:ecg
            }

    def load_record_set_data(self, db_result):
        ecg_col = db_result[cons.COLLECTION_ECG_NAME]
        record_set_col = db_result[cons.COLLECTION_RECORD_SET_NAME]
        count = 0
        list_record_set:list[RecordSet] = []

        data = self.load_record_list_from_record_set(ecg_col, record_set_col)
        
        for record_set in data:
            count = count + 1
            ecg_data = self.retrieve_ecg_data(record_set[cons.CONS_ECG])
            list_record_set.append(RecordSet(
                record_set_name=record_set[cons.CONS_RECORD_SET_NAME],
                source=ecg_data,
                created_date=common.convert_time_to_datetime(record_set[cons.ECG_CREATED_DATE]),
                modified_date=common.convert_time_to_datetime(record_set[cons.ECG_MODIFIED_DATE]),
                id=str(record_set[cons.ECG_ID_SHORT])
            ))

         # Check if there is no imported record in the DB --> If so, return a warning message
        if count < 1:
            st.warning('There is no item. Please check again!')
            st.stop()
            
        header_table = [
            cons.HEADER_RECORD_SET,
            cons.HEADER_SOURCE,
            cons.HEADER_CREATED_DATE,
            cons.HEADER_MODIFIED_DATE,
            cons.HEADER_ID
        ]

        column_names = [
            cons.CONS_RECORD_SET_NAME,
            cons.ECG_SOURCE,
            cons.ECG_CREATED_DATE,
            cons.ECG_MODIFIED_DATE,
            cons.ECG_ID
        ]

        # Clone the list of record set from list_record_set
        # Then, update the source with the "record description"
        df_list_record_set = []
        for x in list_record_set:
            df_list_record_set.append(RecordSet(
                record_set_name=x.record_set_name,
                source=x.source[CONS_ECG_DESC_STR],
                created_date=x.created_date,
                modified_date=x.modified_date,
                id=x.id)
            )

        # Generate data from list ECG records to table of DataFrame
        df = pd.DataFrame.from_records([vars(s) for s in df_list_record_set])
        # Reorder columns of the DataFrame
        df = df.reindex(columns=column_names)
        # Set header names
        df.columns = header_table

        with st.form("record_set_data_form"):
            st.write('### RecordSet Data', df)
            st.info('Total items: ' + str(count))

            selected_indices = st.multiselect('Select rows:', df.index)

            # Every form must have a submit button.
            clicked = st.form_submit_button("Load record")
            if clicked:
                st.session_state.exp_region_load_record = True

            if selected_indices:
                selected_rows = df.loc[selected_indices]
                st.write('### Selected Rows', selected_rows)
            else:
                selected_rows = pd.DataFrame()

        # Count number of selected rows
        number_selected_rows = len(selected_rows.values)

        # Return warning message if there are more than 2 selected items
        if number_selected_rows > 1:
            st.warning('Please select only one item!')
            st.stop()

        # Only process if any item is selected
        if st.session_state.exp_region_load_record and number_selected_rows > 0:
            for index, row in selected_rows.iterrows():
                record_set_id = row[cons.HEADER_ID]
                result = self.get_first_record_set_from_list(list_record_set, record_set_id)
                if result:
                    ecg_result = result.source[CONS_ECG_LIST]
                    self.build_ecg_data(db_result, ecg_result, record_set_id)

    def build_ecg_data(self, db_result, ecg_data, record_set_id):
        count = 0
        list_ecg = []
        for record in ecg_data:
            count = count + 1
            list_ecg.append(ECG(
                source=record[cons.ECG_SOURCE],
                file_name=record[cons.ECG_FILE_NAME],
                channel=common.convert_list_to_string(record[cons.ECG_CHANNEL]).upper(),
                sample=str(record[cons.ECG_SAMPLE]),
                sample_rate=str(record[cons.ECG_SAMPLE_RATE]),
                unit=record[cons.ECG_UNIT],
                comments=record[cons.ECG_COMMENTS],
                ecg=str(record[cons.ECG_ECG]),
                time=str(record[cons.ECG_TIME]),
                created_date=common.convert_time_to_datetime(record[cons.ECG_CREATED_DATE]),
                modified_date=common.convert_time_to_datetime(record[cons.ECG_MODIFIED_DATE]),
                id=str(record[cons.ECG_ID_SHORT])
            ))
        
        # Check if there is no imported record in the DB --> If so, return a warning message
        if count < 1:
            st.warning('There is no item. Please check again!')
            st.stop()

        header_table = [
            cons.HEADER_SOURCE,
            cons.HEADER_FILENAME,
            cons.HEADER_CHANNEL,
            cons.HEADER_SAMPLES,
            cons.HEADER_TIME,
            cons.HEADER_SAMPLE_RATE,
            cons.HEADER_UNIT,
            cons.HEADER_COMMENTS,
            cons.HEADER_ECG,
            cons.HEADER_CREATED_DATE,
            cons.HEADER_MODIFIED_DATE,
            cons.HEADER_ID
        ]

        column_names = [
            cons.ECG_SOURCE,
            cons.ECG_FILE_NAME,
            cons.ECG_CHANNEL,
            cons.ECG_SAMPLE,
            cons.ECG_TIME,
            cons.ECG_SAMPLE_RATE,
            cons.ECG_UNIT,
            cons.ECG_COMMENTS,
            cons.ECG_ECG,
            cons.ECG_CREATED_DATE,
            cons.ECG_MODIFIED_DATE,
            cons.ECG_ID
        ]

        # Generate data from list ECG records to table of DataFrame
        df = pd.DataFrame.from_records([vars(s) for s in list_ecg])
        # Reorder columns of the DataFrame
        df = df.reindex(columns=column_names)
        # Set header names
        df.columns = header_table

        # with st.form("record_data_form"):
        st.write('### Record data by RecordSet', df)
        st.info('Total items: ' + str(count))

        selected_indices = st.multiselect('Select rows:', df.index)

        selected_rows = df.loc[selected_indices]
        st.write('### Selected Rows', selected_rows)

        # Count number of selected rows
        number_selected_rows = len(selected_rows.values)

        # Return warning message if there are more than 2 selected items
        if number_selected_rows > 1:
            st.warning('Please select only one item!')
            st.stop()

        # Every form must have a submit button.
        clicked = st.button("Visualize record")
        if clicked or st.session_state.exp_region_visualize_record:
            st.session_state.exp_region_visualize_record = True
            self.visualize_data(db_result, selected_rows, record_set_id)


    def visualize_data(self, db_result, selected_rows, record_set_id):
        with st.form("exporting_region_form"):
            st.write('### Create exporting region')
            for index, row in selected_rows.iterrows():
                record_id = ObjectId(row[cons.HEADER_ID])

                # Start and end times
                start_time = st.number_input(cons.CONS_START_TIME,min_value=0,step=1)
                end_time = st.number_input(cons.CONS_END_TIME,min_value=1,step=1,value=5)
                
            save_clicked = st.form_submit_button("Save")
            if save_clicked:
                exporting_region_data = ExportingRegion(
                    record_set_id=ObjectId(record_set_id),
                    ecg_id=record_id,
                    start_time=start_time,
                    end_time=end_time
                )

                # Get Exporting Region Collection
                exporting_region_col = db_result[cons.COLLECTION_EXPORTING_REGION_NAME]
                
                # Save the exporting region to DB
                exporting_region_id = exporting_region_scraper.add_exporting_region(exporting_region_col, exporting_region_data)
                # Check if the record is succsessfully created
                if exporting_region_id:
                    st.success('Added successfully!')
                else:
                    st.warning('Please try again!')

