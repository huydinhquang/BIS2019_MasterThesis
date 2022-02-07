import streamlit as st
from Controllers.ECGModel import ECG
from Controllers.Configure import Configure
import Controllers.Constants as cons

config = Configure()
configure = config.get_configure_value()

def load_form():
    new_channel = st.text_input(label='Channel name')
    add_clicked = st.button('Add')
    load_list_clicked = st.sidebar.button('Load list channels')
    return new_channel, add_clicked, load_list_clicked