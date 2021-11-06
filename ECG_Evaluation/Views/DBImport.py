import streamlit as st

def load_form():
    folder_source = st.text_input(label='Please add a folder:', value="C:/Users/HuyDQ/OneDrive/HuyDQ/OneDrive/MasterThesis/Thesis/DB/PTB")
    clicked = st.button('Get file')
    return folder_source, clicked