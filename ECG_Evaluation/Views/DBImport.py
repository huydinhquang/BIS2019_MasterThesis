import streamlit as st
from Controllers.ECGModel import ECG

def load_form():
    folder_source = st.text_input(label='Please enter a folder:', value="C:/Users/HuyDQ/OneDrive/HuyDQ/OneDrive/MasterThesis/Thesis/DB/PTB")
    clicked = st.button('Get file')
    return folder_source, clicked

def render_property(ecg_property : ECG):
    col1, col2 = st.columns(2)
    with col1:
        source = st.text_input('Source name', 'Test')
        channel = st.multiselect('Channel(s)',ecg_property.channel,ecg_property.channel)
    with col2:
        # sample_rate = st.slider('Sample rate', 0, 10000,
        #                        ecg_property.sample_rate)
        st.text('Sample rate: ' + str(ecg_property.sample_rate))
        st.text('Total records: ' + str(ecg_property.record))
        st.text('Time(s): ' + str(ecg_property.time))
        st.text('Total channels: ' + str(len(ecg_property.channel)))
    return source, channel
