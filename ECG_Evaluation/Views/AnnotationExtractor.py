import streamlit as st

def load_form():
    list_channel = st.sidebar.multiselect(
            'Channel(s)',
            ['I', 'II', 'III',
             'aVR', 'aVL', 'aVF',
             'V1', 'V2', 'V3',
             'V4', 'V5', 'V6',
             'Vx', 'Vy', 'Vz'])
    filter_source = st.sidebar.button('Filter source')
    # sample_rate = st.sidebar.number_input('Sample rate', min_value=0,max_value=10000,value=1000)
    # export_unit = st.sidebar.number_input('Export unit', min_value=0, max_value=10000, value=10)
    # return list_channel, sample_rate, export_unit, filter_source
    return list_channel, filter_source

def render_download_section():
    folder_download = st.text_input(label='Downloadable folder:', value="C:/Users/HuyDQ/OneDrive/HuyDQ/OneDrive/MasterThesis/Thesis/DB/Download")
    if folder_download:
        clicked = st.button('Download files')
        return folder_download, clicked

def render_resample_signal():
    clicked = st.button('Resample signals')
    return clicked        