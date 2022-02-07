import streamlit as st
from Controllers.ECGModel import ECG
from Controllers.Configure import Configure
import Controllers.Constants as cons

config = Configure()
configure = config.get_configure_value()

def load_form():
    slider_value, manual_inp_val = st.columns([0.75,0.25])
    with slider_value:
        val_target_sample_rate = st.slider('Target sample rate slider', 
                        min_value = 1,
                        max_value = 2000,
                        value=500,
                        step = 1)
        val_duration = st.slider('Duration slider', 
                        min_value = 1,
                        max_value = 60,
                        value=5,
                        step = 1)
    with manual_inp_val:
        target_sample_rate = int(st.number_input('Target sample rate text', value=val_target_sample_rate))
        duration = int(st.number_input('Duration text', value=val_duration))
    return target_sample_rate, duration

def load_button():
    add_clicked = st.button('Create')
    load_list_clicked = st.sidebar.button('Load list template')
    return add_clicked, load_list_clicked