import streamlit as st
import Controllers.Constants as cons

mongo = st.secrets[cons.MONGOCONNECTIONSTR]
db_name = st.secrets[cons.MONGODB][cons.DB_NAME]
collection_main_name = st.secrets[cons.MONGODB][cons.COLLECTION_MAIN_NAME]
# collection_channel_name = st.secrets[cons.MONGODB][cons.COLLECTION_CHANNEL_NAME]