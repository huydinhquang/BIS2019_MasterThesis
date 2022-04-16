from bson.objectid import ObjectId
from pymongo import helpers
import streamlit as st
from Controllers.ECGModel import ECG
import wfdb
from datetime import datetime
import pandas as pd
import Controllers.Constants as cons
import Controllers.Common as common
from Controllers.RecordSetModel import RecordSet
import Views.DownloadChannel as download_channel
import Scraper as scraper
import Scrapers.RecordSetScraper as record_set_scraper

class ExportDataProcessor:
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
                # source=record[cons.ECG_SOURCE],
                created_date=common.convert_time_to_datetime(record[cons.CONS_CREATED_DATE]),
                modified_date=common.convert_time_to_datetime(record[cons.CONS_MODIFIED_DATE]),
                id=str(record[cons.ECG_ID_SHORT])
            ))
            
        header_table = [
            cons.HEADER_RECORD_SET,
            cons.HEADER_SOURCE,
            cons.HEADER_CREATED_DATE,
            cons.HEADER_MODIFIED_DATE,
            cons.HEADER_ID
        ]

        df = pd.DataFrame.from_records([vars(s) for s in list_record_set])
        df.columns = header_table

        st.write('### Full Dataset', df)
        st.info('Total items: ' + str(count))

        # source_name, filter_source_clicked = download_channel.filter_source()
        # if filter_source_clicked:
        #     st.session_state.filter_source = True

        # if st.session_state.filter_source:
        #     df = df[df['Source'].str.contains(source_name, na=False, case=False)]
        #     # st.dataframe(df)
        
        # selected_indices = st.multiselect('Select rows:', df.index)
        # if selected_indices or st.session_state.load_source_list:
        #     st.session_state.load_source_list = True
        #     # st.session_state.get_select_source = True
        #     selected_rows = df.loc[selected_indices]
        #     st.write('### Selected Rows', selected_rows)

        #     record_set_name, region_start, region_end, create_clicked = download_channel.record_set()
        #     if create_clicked:
        #         list_selected_ecg = []
        #         for index, row in selected_rows.iterrows():
        #             list_selected_ecg.append(ObjectId(row[cons.HEADER_ID]))
        #         if len(list_selected_ecg) > 0:
        #             record_set_id = record_set_scraper.add_record_set(record_set_col, record_set_name, list_selected_ecg)
        #             return record_set_id
