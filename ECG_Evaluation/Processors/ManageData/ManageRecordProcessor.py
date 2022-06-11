from bson.objectid import ObjectId
import numpy as np
import streamlit as st
from Controllers.ECGModel import ECG
import pandas as pd
import Controllers.Constants as cons
import Controllers.Common as common
import Scraper as scraper
import Scrapers.ManageData.ManageRecordScraper as manage_record_scraper
import Controllers.Helper as helper

class ManageRecordProcessor:
    def load_record_data(self, db_result):
        ecg_col = db_result[cons.COLLECTION_ECG_NAME]
        count = 0
        list_ecg = []
        # data = scraper.find_by_query(ecg_col, cons.CONS_QUERYREGEX_STR, cons.ECG_SOURCE, source_name)
        data = scraper.find(ecg_col)

        # Check if there is no imported record in the DB --> If so, return a warning message
        if (data.count() < 1):
            st.warning('There is no record. Please check again!')
            st.stop()

        for record in data:
            count = count + 1
            list_ecg.append(ECG(
                source=record[cons.ECG_SOURCE],
                file_name=record[cons.ECG_FILE_NAME],
                channel=common.convert_list_to_string(record[cons.ECG_CHANNEL]).upper(),
                sample=record[cons.ECG_SAMPLE],
                sample_rate=record[cons.ECG_SAMPLE_RATE],
                unit=record[cons.ECG_UNIT],
                comments=record[cons.ECG_COMMENTS],
                ecg=record[cons.ECG_ECG],
                time=record[cons.ECG_TIME],
                created_date=common.convert_time_to_datetime(record[cons.ECG_CREATED_DATE]),
                modified_date=common.convert_time_to_datetime(record[cons.ECG_MODIFIED_DATE]),
                id=str(record[cons.ECG_ID_SHORT])
            ))
            
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

        with st.form("record_data_form"):
            st.write('### Full Dataset', df)
            st.info('Total items: ' + str(count))

            selected_indices = st.multiselect('Select rows:', df.index)

            # Every form must have a submit button.
            clicked = st.form_submit_button("Load record")
            if clicked:
                st.session_state.manage_record = True

            if selected_indices:
                selected_rows = df.loc[selected_indices]
                st.write('### Selected Rows', selected_rows)
            else:
                selected_rows = pd.DataFrame()

        # Count number of selected rows
        number_selected_rows = len(selected_rows.values)
        # Only process if any item is selected
        if st.session_state.manage_record and number_selected_rows > 0:
            col1, col2 = st.columns([.1,1])
            with col1:
                edit_clicked = st.button("Edit")                
                
            with col2:
                delete_clicked = st.button("Delete")
                
            if edit_clicked or st.session_state.edit_record:
                st.session_state.edit_record = True
                if number_selected_rows == 1:
                    self.edit_record(db_result, ecg_col, selected_rows)
                else:
                    st.warning("Please select one item to edit at the time!")
            if delete_clicked or st.session_state.delete_record:
                st.session_state.delete_record = True
                st.warning("Are you sure you want to delete the record(s)?")
                confirm_clicked = st.button("Yes")
                if confirm_clicked:
                    self.delete_record(db_result, ecg_col, selected_rows)

    def delete_record(self, db_result, ecg_col, selected_rows):
        count = 0
        db= db_result[cons.DB_NAME]
        file_fs = scraper.connect_gridfs(db)
        for index, row in selected_rows.iterrows():
            # Get record id
            record_id = ObjectId(row[cons.HEADER_ID])
            # Delete ECG record
            result_record = manage_record_scraper.delete_record(ecg_col, cons.FILE_ID_SHORT, record_id)
            # Check if the record is succsessfully deleted
            if result_record > 0:
                # Delete ECG files with related data (files and chunks collections)
                manage_record_scraper.delete_ecg_file(db, file_fs, cons.FILE_ECG_ID, record_id)
                count = count + 1
        st.success(f'Delete successfully {count} items! Please refresh the result.')

    def edit_record(self, db_result, ecg_col, selected_rows):
        with st.form("edit_record_form"):
            st.write('### Edit record')
            for index, row in selected_rows.iterrows():
                record_id = ObjectId(row[cons.HEADER_ID])

                # Source name
                if row[cons.HEADER_COMMENTS]:
                    source_name = st.text_input(cons.CONS_SOURCE_NAME, value=row[cons.HEADER_SOURCE])
                else:
                    source_name = st.text_input(cons.CONS_SOURCE_NAME)
                
                # Channels
                channel = st.text_input(label=cons.CONS_CHANNELS, value=row[cons.HEADER_CHANNEL])
                channel_guideline = '<p style="font-family:Source Sans Pro, sans-serif; color:orange; font-size: 15px;">Each channels is separated by a semicolon. Ex: I;II;III</p>'
                st.markdown(channel_guideline, unsafe_allow_html=True)

                # Total channels
                total_channels = len(common.convert_string_to_list(row[cons.HEADER_CHANNEL], cons.CONS_SEMICOLON, True))
                st.text(f'{cons.CONS_TOTAL_CHANNELS}: {str(total_channels)}')

                # Sample rate
                sample_rate = st.number_input(cons.CONS_SAMPLE_RATE,min_value=1,step=1, value=row[cons.HEADER_SAMPLE_RATE])

                # Amplitude Unit
                unit_options = [cons.CONS_UNIT_MV, cons.CONS_UNIT_V]
                unit_index = helper.get_item_index(row[cons.HEADER_UNIT], unit_options)
                unit = st.selectbox(cons.CONS_UNIT, options=unit_options, index=unit_index)

                # Comments
                if row[cons.HEADER_COMMENTS]:
                    comments = st.text_area(cons.CONS_COMMENTS, value=row[cons.HEADER_COMMENTS], height=120)
                else:
                    comments = st.text_area(cons.CONS_COMMENTS, value=cons.CONS_ADD_COMMENTS, height=120)

                # Recalucate the number of samples based on the new sample rates
                samples = np.ceil(sample_rate * row[cons.HEADER_SAMPLES] / row[cons.HEADER_SAMPLE_RATE])

            save_clicked = st.form_submit_button("Save")
            if save_clicked:
                channel_list = common.convert_string_to_list(channel, cons.CONS_SEMICOLON, True)
                new_record_value = ECG(
                    source=source_name,
                    channel=channel_list,
                    sample_rate=sample_rate,
                    unit=unit,
                    comments=comments,
                    sample=samples,
                    is_update=True
                )

                # Update ECG record
                result_record = manage_record_scraper.update_record(ecg_col, cons.FILE_ID_SHORT, record_id, new_record_value)
                # Check if the record is succsessfully updated
                if result_record > 0:
                    db= db_result[cons.DB_NAME]
                    # Update ECG files with related data 
                    result_file = manage_record_scraper.update_ecg_file(db, cons.FILE_ECG_ID, record_id, new_record_value)
                    # Check if the file is succsessfully updated
                    if result_file > 0:
                        st.success('Save successfully! Please refresh the result.')

