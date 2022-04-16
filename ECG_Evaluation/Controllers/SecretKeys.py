import streamlit as st
import Controllers.Constants as cons

mongo = st.secrets[cons.MONGOCONNECTIONSTR]
db_name = st.secrets[cons.MONGODB][cons.DB_NAME]
collection_ecg_name = st.secrets[cons.MONGODB][cons.COLLECTION_ECG_NAME]
collection_channel_name = st.secrets[cons.MONGODB][cons.COLLECTION_CHANNEL_NAME]
collection_record_set_name = st.secrets[cons.MONGODB][cons.COLLECTION_RECORD_SET_NAME]
collection_template_exportation_name = st.secrets[cons.MONGODB][cons.COLLECTION_TEMPLATE_EXPORTATION_NAME]

format_descriptor = st.secrets[cons.CONFIGURE][cons.FORMAT_DESCRIPTOR]
channel_name = st.secrets[cons.CONFIGURE][cons.CHANNEL_NAME]