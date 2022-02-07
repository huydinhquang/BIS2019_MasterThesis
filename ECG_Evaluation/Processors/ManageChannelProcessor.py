import streamlit as st
import pandas as pd
import Controllers.Constants as cons
import Scraper as scraper
import Controllers.Common as common

class ManageChannelProcessor:
    def load_list_channel(self, my_col):
        # st.session_state.load_channel_list = True
        count = 0
        list_channel = []
        data = scraper.find(my_col)
        for record in data:
            count = count + 1
            list_channel.append(
                {
                    "channel": record[cons.CONS_CHANNEL],
                    "created_date":common.convert_time_to_datetime(record[cons.CONS_CREATED_DATE]),
                    "modified_date":common.convert_time_to_datetime(record[cons.CONS_MODIFIED_DATE]),
                    "id":str(record[cons.CONS_ID_SHORT])
                }
            )
            
        header_table = [
            cons.HEADER_CHANNEL,
            cons.HEADER_CREATED_DATE,
            cons.HEADER_MODIFIED_DATE,
            cons.HEADER_ID
        ]

        # df = pd.DataFrame(list_channel, columns=header_table)
        # df.columns = header_table
        df = pd.DataFrame(list_channel)

        st.write('### Full Dataset', df)
        st.info('Total items: ' + str(count))
        selected_indices = st.multiselect('Select rows:', df.index)
        if selected_indices or st.session_state.load_channel_list:
            st.session_state.load_channel_list = True
            # st.session_state.get_select_source = True
            selected_rows = df.loc[selected_indices]
            st.write('### Selected Rows', selected_rows)
            return selected_rows