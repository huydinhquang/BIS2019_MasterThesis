import streamlit as st
from Controllers.Configure import Configure
import Controllers.Constants as cons

config = Configure()
configure = config.get_configure_value()

def load_form():
    load_record_list_clicked = st.sidebar.button('Load record list')
    return load_record_list_clicked

def filter_record():
    source_name = st.text_input('Source name')
    filter_record_clicked = st.button('Filter source')
    return source_name, filter_record_clicked

def record_set():
    st.write('### Record set creation')
    with st.form('record_set_creation'):
        record_set_name = st.text_input('Record set name')
        create_clicked = st.form_submit_button('Create')
        return record_set_name, create_clicked

def render_resample_signal():
    clicked = st.button('Resample signals')
    return clicked        