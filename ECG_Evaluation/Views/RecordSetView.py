import streamlit as st

def load_form():
    # list_channel = st.sidebar.multiselect(
    #         'Channel(s)',
    #         ['I', 'II', 'III',
    #          'aVR', 'aVL', 'aVF',
    #          'V1', 'V2', 'V3',
    #          'V4', 'V5', 'V6',
    #          'Vx', 'Vy', 'Vz'])
    # source_name = st.sidebar.text_input('Source name')
    load_source_list_clicked = st.sidebar.button('Load source list')
    # with st.sidebar.form("my_form"):
    #     a = st.slider('sidebar for testing', 5, 10, 9)
    #     calculate = st.form_submit_button('Calculate')
    # sample_rate = st.sidebar.number_input('Sample rate', min_value=0,max_value=10000,value=1000)
    # export_unit = st.sidebar.number_input('Export unit', min_value=0, max_value=10000, value=10)
    # return list_channel, sample_rate, export_unit, filter_source
    return load_source_list_clicked

def filter_source():
    source_name = st.text_input('Source name')
    filter_source_clicked = st.button('Filter source')
    return source_name, filter_source_clicked

def record_set():
    st.write('### Record set creation')
    with st.form('Record set creation'):
        record_set_name = st.text_input('Record set name')
        region_start = st.number_input('Region start', min_value=0)
        region_end = st.number_input('Region end', min_value=0)
        create_clicked = st.form_submit_button('Create')
        return record_set_name, region_start, region_end, create_clicked

def render_download_section():
    folder_download = st.text_input(label='Downloadable folder:', value="C:/Users/HuyDQ/OneDrive/HuyDQ/OneDrive/MasterThesis/Thesis/DB/Download")
    if folder_download:
        clicked = st.button('Download files')
        return folder_download, clicked

def render_resample_signal():
    clicked = st.button('Resample signals')
    return clicked        