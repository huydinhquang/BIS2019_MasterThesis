import streamlit as st
from Controllers.ECGModel import ECG
from Controllers.Configure import Configure
import Controllers.Constants as cons

config = Configure()
configure = config.get_configure_value()

def load_form():
    # new_channel = st.text_input(label='Record name')
    load_data_clicked = st.sidebar.button('Load data')
    return load_data_clicked