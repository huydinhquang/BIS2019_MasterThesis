import streamlit as st
from Controllers.ECGModel import ECG
from Controllers.Configure import Configure
import Controllers.Constants as cons

config = Configure()
configure = config.get_configure_value()

def load_form():
    folder_source = st.text_input(label='Please enter a folder:', value="C:/Users/HuyDQ/OneDrive/HuyDQ/OneDrive/MasterThesis/Thesis/DB/PTB")
    format_desc = st.selectbox('Format descriptor', configure[cons.FORMAT_DESCRIPTOR])
    clicked = st.button('Retrieve property')
    return folder_source, format_desc, clicked

def render_property(ecg_property : ECG, total_channels):
    col1, col2 = st.columns(2)
    with col1:
        # File name
        source = st.text_input('Source name', ecg_property.file_name)

        # Channels
        if ecg_property.channel:
            channel = st.multiselect('Channel(s)',ecg_property.channel,ecg_property.channel)
        else:
            channel = st.multiselect('Channel(s)', configure[cons.CHANNEL_NAME])
        
        # Total channels
        total_channels = st.text('Total channels: ' + str(total_channels))
    with col2:
        # sample_rate = st.slider('Sample rate', 0, 10000,
        #                        ecg_property.sample_rate)
        
        # Sample rate
        if ecg_property.sample_rate:
            sample_rate = ecg_property.sample_rate
            st.text('Sample rate: ' + str(sample_rate))
        else:
            sample_rate = st.number_input('Sample rate',min_value=1,step=1)

        # Time
        if ecg_property.time:
            time = ecg_property.time
            st.text('Time(s): ' + str(time))
        else:
            time = st.number_input('Time(s)',min_value=1,step=1)
        
        # Sample
        st.text('Samples: ' + str(len(ecg_property.sample)))
    result = {
        cons.ECG_SOURCE: source,
        cons.ECG_CHANNEL: channel,
        cons.ECG_SAMPLE_RATE: sample_rate,
        cons.ECG_TIME: time,
        cons.ECG_TOTAL_CHANNELS: total_channels
    }
    return result
