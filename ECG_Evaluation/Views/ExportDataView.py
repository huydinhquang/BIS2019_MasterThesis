import streamlit as st
from Controllers.Configure import Configure
import Controllers.Constants as cons

config = Configure()
configure = config.get_configure_value()

def load_form():
    load_data_clicked = st.sidebar.button('Load data')
    return load_data_clicked

def load_form1():    
    folder_source = st.text_input(label='Please enter a folder:', value=configure[cons.CONF_FOLDER_EXPORT_DATA])
    clicked = st.button('Load sources')
    return folder_source, clicked
