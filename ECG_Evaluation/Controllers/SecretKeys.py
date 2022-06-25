import streamlit as st
import Controllers.Constants as cons

mongo = st.secrets[cons.MONGOCONNECTIONSTR]
db_name = st.secrets[cons.MONGODB][cons.DB_NAME]
collection_ecg_name = st.secrets[cons.MONGODB][cons.COLLECTION_ECG_NAME]
collection_channel_name = st.secrets[cons.MONGODB][cons.COLLECTION_CHANNEL_NAME]
collection_record_set_name = st.secrets[cons.MONGODB][cons.COLLECTION_RECORD_SET_NAME]
collection_exporting_template_name = st.secrets[cons.MONGODB][cons.COLLECTION_EXPORTING_TEMPLATE_NAME]
collection_exporting_region_name  = st.secrets[cons.MONGODB][cons.COLLECTION_EXPORTING_REGION_NAME]

format_descriptor = st.secrets[cons.CONFIGURE][cons.CONF_FORMAT_DESCRIPTOR]
channel_name = st.secrets[cons.CONFIGURE][cons.CONF_CHANNEL_NAME]
default_folder_import_record = st.secrets[cons.CONFIGURE][cons.CONF_FOLDER_IMPORT_RECORD]
default_folder_import_record_mass = st.secrets[cons.CONFIGURE][cons.CONF_FOLDER_IMPORT_RECORD_MASS]
default_folder_export_data = st.secrets[cons.CONFIGURE][cons.CONF_FOLDER_EXPORT_DATA]
