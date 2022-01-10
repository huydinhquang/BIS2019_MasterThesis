import streamlit as st
from Controllers.ECGModel import ECG
from Controllers.Configure import Configure
import Controllers.Constants as cons
import Views.DBImport as db_import

config = Configure()
configure = config.get_configure_value()

def load_form():
    folder_source = st.text_input(label='Please enter a folder:', value=f"C:/Users/HuyDQ/OneDrive/HuyDQ/OneDrive/MasterThesis/Thesis/DB/Download")
    clicked = st.button('Load sources')
    return folder_source, clicked

