import streamlit as st
from Controllers.ECGModel import ECG
from Controllers.Configure import Configure
import Controllers.Constants as cons

config = Configure()
configure = config.get_configure_value()

def load_form():
    folder_source = st.text_input(label='Please enter a folder:', value="C:/Users/HuyDQ/OneDrive/HuyDQ/OneDrive/MasterThesis/Thesis/DB/PTB")
    format_desc = st.selectbox('Format descriptor', configure[cons.FORMAT_DESCRIPTOR])
    retrieve_clicked = st.button('Retrieve property')
    return folder_source, format_desc, retrieve_clicked

def render_property(ecg_property : ECG, total_channels):
    col1, col2 = st.columns(2)
    with col1:
        # File name
        source = st.text_input('Source name', ecg_property.file_name)

        # Channels
        if ecg_property.channel:
            channel = st.multiselect('Channel(s)',ecg_property.channel,ecg_property.channel)
            is_channel_from_record = True
        else:
            channel = st.text_input(label='Channel(s)')
            is_channel_from_record = False
            channel_guideline = '<p style="font-family:Source Sans Pro, sans-serif; color:orange; font-size: 15px;">Each channels is separated by a semicolon. Ex: I;II;III</p>'
            st.markdown(channel_guideline, unsafe_allow_html=True)

        # Total channels
        total_channels = st.text(f'Total channels: {str(total_channels)}')
    with col2:
        # sample_rate = st.slider('Sample rate', 0, 10000,
        #                        ecg_property.sample_rate)
        
        # Sample rate
        if ecg_property.sample_rate:
            sample_rate = ecg_property.sample_rate
            st.text(f'Sample rate: {str(sample_rate)}')
        else:
            sample_rate = st.number_input('Sample rate',min_value=1,step=1)

        # Time
        if ecg_property.time:
            time = ecg_property.time
            st.text(f'Time(s): {str(time)}')
        else:
            time = st.number_input('Time(s)',min_value=1,step=1)
        
        # Sample
        st.text(f'Samples: {str(len(ecg_property.sample))}')

        # Amplitude Unit
        unit = st.selectbox('Unit', options=ecg_property.unit)

        # Description
        comments = st.text_area('Comments', 'Add any comments here', height=120)

    result = {
        cons.ECG_SOURCE: source,
        cons.ECG_CHANNEL: channel,
        cons.ECG_CHANNEL_TEXT: is_channel_from_record,
        cons.ECG_SAMPLE_RATE: sample_rate,
        cons.ECG_TIME: time,
        cons.ECG_TOTAL_CHANNELS: total_channels,
        cons.ECG_UNIT: unit,
        cons.ECG_COMMENTS: comments
    }
    return result
