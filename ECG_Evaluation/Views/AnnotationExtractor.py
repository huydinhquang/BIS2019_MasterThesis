import streamlit as st

def load_form():
    list_channel = st.sidebar.multiselect(
            'Channel(s)',
            ['I', 'II', 'III',
             'aVR', 'aVL', 'aVF',
             'V1', 'V2', 'V3',
             'V4', 'V5', 'V6',
             'Vx', 'Vy', 'Vz'])
    return list_channel