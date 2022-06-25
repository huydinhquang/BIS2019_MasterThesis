from bson.objectid import ObjectId
import streamlit as st
from Controllers.ECGModel import ECG
import pandas as pd
import Controllers.Constants as cons
import Controllers.Common as common
import Views.RecordSetView as record_set_view
import Scraper as scraper
import Scrapers.RecordSetScraper as record_set_scraper

class RecordSetProcessor:
    def load_record_set_data(self, db_result):
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
                created_date=common.convert_time_to_datetime(record[cons.ECG_CREATED_DATE]),
                modified_date=common.convert_time_to_datetime(record[cons.ECG_MODIFIED_DATE]),
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

        st.write('### Full Dataset', df)
        st.info('Total items: ' + str(count))

        # source_name, filter_record_clicked = download_channel.filter_record()
        # if filter_record_clicked:
        #     st.session_state.filter_record = True

        # if st.session_state.filter_record:
        #     df = df[df['Source'].str.contains(source_name, na=False, case=False)]
        #     # st.dataframe(df)
        
        selected_indices = st.multiselect('Select rows:', df.index)
        if selected_indices or st.session_state.load_record_list:
            st.session_state.load_record_list = True
            # st.session_state.get_select_source = True
            selected_rows = df.loc[selected_indices]
            st.write('### Selected Rows', selected_rows)

            record_set_name, create_clicked = record_set_view.record_set()
            if create_clicked:
                list_selected_ecg = []
                for index, row in selected_rows.iterrows():
                    list_selected_ecg.append(ObjectId(row[cons.HEADER_ID]))
                if len(list_selected_ecg) > 0:
                    record_set_id = record_set_scraper.add_record_set(record_set_col, record_set_name, list_selected_ecg)
                    if record_set_id:
                        st.success('Added successfully!')
                    else:
                        st.warning('Please try again!')
