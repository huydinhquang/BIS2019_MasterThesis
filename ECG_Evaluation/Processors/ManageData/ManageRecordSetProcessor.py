from bson.objectid import ObjectId
import numpy as np
import streamlit as st
from Controllers.RecordSetModel import RecordSet
import pandas as pd
import Controllers.Constants as cons
import Controllers.Common as common
import Scraper as scraper
import Scrapers.ManageData.ManageRecordSetScraper as manage_record_set_scraper
import Controllers.Helper as helper
from Controllers.ECGModel import ECG

class ManageRecordSetProcessor:
    def load_record_list_from_record_set(self, ecg_col, record_set_col):
        query_data = {
            cons.CONS_QUERY_FROM : ecg_col.name,
            cons.CONS_QUERY_LOCALFIELD: cons.ECG_SOURCE,
            cons.CONS_QUERY_FOREIGNFIELD: cons.CONS_ID_SHORT,
            cons.CONS_QUERY_AS: ecg_col.name
        }
        result = manage_record_set_scraper.find_record_list(record_set_col, query_data)
        return result

    def retrieve_ecg_data(self, ecg:list[ECG]):
        ecg_list = []
        for x in ecg:
            ecg_list.append(f'Source: {x[cons.ECG_SOURCE]} - File name: {x[cons.ECG_FILE_NAME]}')
        ecg_str = f'{cons.CONS_SEMICOLON} '.join(ecg_list)
        return ecg_str

    def load_record_data(self, db_result):
        ecg_col = db_result[cons.COLLECTION_ECG_NAME]
        record_set_col = db_result[cons.COLLECTION_RECORD_SET_NAME]
        count = 0
        list_record_set = []

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

        # Generate data from list ECG records to table of DataFrame
        df = pd.DataFrame.from_records([vars(s) for s in list_record_set])
        # Reorder columns of the DataFrame
        df = df.reindex(columns=column_names)
        # Set header names
        df.columns = header_table

        with st.form("record_set_data_form"):
            st.write('### Full Dataset', df)
            st.info('Total items: ' + str(count))

            selected_indices = st.multiselect('Select rows:', df.index)

            # Every form must have a submit button.
            clicked = st.form_submit_button("Load record")
            if clicked:
                st.session_state.manage_record_set = True

            if selected_indices:
                selected_rows = df.loc[selected_indices]
                st.write('### Selected Rows', selected_rows)
            else:
                selected_rows = pd.DataFrame()

        # Count number of selected rows
        number_selected_rows = len(selected_rows.values)
        # Only process if any item is selected
        if st.session_state.manage_record_set and number_selected_rows > 0:
            col1, col2 = st.columns([.1,1])
            with col1:
                edit_clicked = st.button("Edit")                
                
            with col2:
                delete_clicked = st.button("Delete")
                
            if edit_clicked or st.session_state.edit_record_set:
                st.session_state.edit_record_set = True
                if number_selected_rows == 1:
                    self.edit_record_set(record_set_col, selected_rows)
                else:
                    st.warning("Please select one item to edit at the time!")
            if delete_clicked or st.session_state.delete_record_set:
                st.session_state.delete_record_set = True
                st.warning("Are you sure you want to delete the record set(s)?")
                confirm_clicked = st.button("Yes")
                if confirm_clicked:
                    self.delete_record_set(record_set_col, selected_rows)

    def delete_record_set(self, record_set_col, selected_rows):
        count = 0
        for index, row in selected_rows.iterrows():
            # Get record id
            record_id = ObjectId(row[cons.HEADER_ID])
            # Delete ECG record
            result_record = manage_record_set_scraper.delete_record_set(record_set_col, cons.FILE_ID_SHORT, record_id)
            # Check if the record is succsessfully deleted
            if result_record > 0:
                count = count + 1
        st.success(f'Delete successfully {count} items! Please refresh the result.')

    def edit_record_set(self, record_set_col, selected_rows):
        with st.form("edit_record_set_form"):
            st.write('### Edit record set')
            for index, row in selected_rows.iterrows():
                record_id = ObjectId(row[cons.HEADER_ID])

                # RecordSet name
                record_set_name = st.text_input(cons.HEADER_RECORD_SET, value=row[cons.HEADER_RECORD_SET])
                
            save_clicked = st.form_submit_button("Save")
            if save_clicked:
                new_record_set_value = RecordSet(
                    record_set_name=record_set_name,
                    is_update=True
                )

                # Update Record set
                result_record = manage_record_set_scraper.update_record_set(record_set_col, cons.FILE_ID_SHORT, record_id, new_record_set_value)
                # Check if the record is succsessfully updated
                if result_record > 0:
                    st.success('Save successfully! Please refresh the result.')

