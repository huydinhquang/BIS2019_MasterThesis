import streamlit as st

def load_form():
    load_record_list_clicked = st.sidebar.button('Load record list')
    return load_record_list_clicked

def filter_record():
    source_name = st.text_input('Source name')
    filter_record_clicked = st.button('Filter source')
    return source_name, filter_record_clicked

def record_set():
    st.write('### Record set creation')
    with st.form('Record set creation'):
        record_set_name = st.text_input('Record set name')
        # region_start = st.number_input('Region start', min_value=0)
        # region_end = st.number_input('Region end', min_value=0)
        create_clicked = st.form_submit_button('Create')
        return record_set_name, create_clicked

def render_download_section():
    folder_download = st.text_input(label='Downloadable folder:', value="C:/Users/HuyDQ/OneDrive/HuyDQ/OneDrive/MasterThesis/Thesis/DB/Download")
    if folder_download:
        clicked = st.button('Download files')
        return folder_download, clicked

def render_resample_signal():
    clicked = st.button('Resample signals')
    return clicked        