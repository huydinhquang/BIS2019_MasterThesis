from bson.objectid import ObjectId
import streamlit as st
from Controllers.ECGModel import ECG
import pandas as pd
import Controllers.Constants as cons
import Controllers.Common as common
import Scraper as scraper
import Scrapers.RecordSetScraper as record_set_scraper
import Controllers.Helper as helper

class ManageRecordProcessor:
    def load_record_data(self, db_result):
        ecg_col = db_result[cons.COLLECTION_ECG_NAME]
        record_set_col = db_result[cons.COLLECTION_RECORD_SET_NAME]
        # st.session_state.select_row = True
        count = 0
        list_ecg = []
        # data = scraper.find_by_query(ecg_col, cons.CONS_QUERYREGEX_STR, cons.ECG_SOURCE, source_name)
        data = scraper.find(ecg_col)
        for record in data:
            count = count + 1
            list_ecg.append(ECG(
                source=record[cons.ECG_SOURCE],
                file_name=record[cons.ECG_FILE_NAME],
                channel=common.convert_list_to_string(record[cons.ECG_CHANNEL]).upper(),
                sample=record[cons.ECG_SAMPLE],
                time=record[cons.ECG_TIME],
                sample_rate=record[cons.ECG_SAMPLE_RATE],
                unit=record[cons.ECG_UNIT],
                comments=record[cons.ECG_COMMENTS],
                ecg=record[cons.ECG_ECG],
                created_date=common.convert_timestamp_to_datetime(record[cons.ECG_CREATED_DATE]),
                modified_date=common.convert_timestamp_to_datetime(record[cons.ECG_MODIFIED_DATE]),
                id=str(record[cons.ECG_ID_SHORT]),
                channel_index=None
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
            cons.HEADER_ID,
            cons.HEADER_CHANNEL_INDEX
        ]

        df = pd.DataFrame.from_records([vars(s) for s in list_ecg])
        df.columns = header_table

        with st.form("extract_data_form"):
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

        number_selected_rows = len(selected_rows.values)
        if st.session_state.manage_record and number_selected_rows > 0:
            col1, col2 = st.columns([.1,1])
            with col1:
                edit_clicked = st.button("Edit")                
                
            with col2:
                delete_clicked = st.button("Delete")
                
            if edit_clicked:
                if number_selected_rows == 1:
                    self.edit_record(ecg_col, selected_rows)
                else:
                    st.warning("Please select one item to edit at the time!")
            if delete_clicked:
                st.warning("Are you sure you want to delete the record(s)?")
                if st.button("Yes"):
                    print('Deleted!')

    def edit_record(self, ecg_col, selected_rows):
        with st.form("edit_record_form"):
            st.write('### Edit record')
            for index, row in selected_rows.iterrows():
                record_id = ObjectId(row[cons.HEADER_ID])

                # Source name
                if row[cons.HEADER_COMMENTS]:
                    source_name = st.text_input(cons.CONS_SOURCE_NAME, value=row[cons.HEADER_SOURCE])
                else:
                    source_name = st.text_input(cons.CONS_SOURCE_NAME)
                
                # File name
                file_name = st.text_input(cons.CONS_FILE_NAME, row[cons.HEADER_FILENAME])

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

            save_clicked = st.form_submit_button("Save")
            if save_clicked:
                channel_list = common.convert_string_to_list(channel, cons.CONS_SEMICOLON, True)
                new_record_value = ECG(
                    source=source_name,
                    file_name=file_name,
                    channel=channel_list,
                    sample_rate=sample_rate,
                    unit=unit,
                    comments=comments
                )
                scraper.update_item(ecg_col, cons.FILE_ID_SHORT, record_id, new_record_value)
