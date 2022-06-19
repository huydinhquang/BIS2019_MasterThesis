import streamlit as st
from Controllers.Configure import Configure

def load_form():
    load_data_clicked = st.sidebar.button('Load data')
    return load_data_clicked