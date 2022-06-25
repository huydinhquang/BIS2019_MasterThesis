import streamlit as st
from Controllers.Configure import Configure
import Controllers.Constants as cons

config = Configure()
configure = config.get_configure_value()

def load_form():
    load_data_clicked = st.sidebar.button('Load data')
    return load_data_clicked

def load_button():
    add_clicked = st.button('Create')
    load_list_clicked = st.sidebar.button('Load list template')
    return add_clicked, load_list_clicked