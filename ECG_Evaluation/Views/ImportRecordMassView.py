import streamlit as st
from Controllers.Configure import Configure
import Controllers.Constants as cons

config = Configure()
configure = config.get_configure_value()

def load_form():
    folder_source = st.text_input(label='Please enter a folder:', value=configure[cons.CONF_FOLDER_IMPORT_RECORD_MASS])
    format_desc = st.selectbox('Format descriptor', configure[cons.CONF_FORMAT_DESCRIPTOR])
    retrieve_clicked = st.button('Retrieve property')
    return folder_source, format_desc, retrieve_clicked

def render_property():
    result = None
    with st.form("import_record_mass_form"):
        mass_import_guideline = '<p style="font-family:Source Sans Pro, sans-serif; color:orange; font-size: 15px;">Please note that \'Mass Import\' will use the following attributes for all records if any of them is missing.</p>'
        st.markdown(mass_import_guideline, unsafe_allow_html=True)
        source = st.text_input('Source')
        comments = st.text_area('Comments', 'Add any comments here', height=120)
        
        channel = st.text_input(label='Channel(s)')
        channel_guideline = '<p style="font-family:Source Sans Pro, sans-serif; color:orange; font-size: 15px;">Each channels is separated by a semicolon. Ex: I;II;III</p>'
        st.markdown(channel_guideline, unsafe_allow_html=True)
        sample_rate = st.number_input('Sample rate',min_value=500,step=1)
        unit = st.selectbox('Unit', options=[cons.CONS_UNIT_MV, cons.CONS_UNIT_V])
        
        # Every form must have a submit button.
        submitted = st.form_submit_button("Mass Import")
        if submitted:
            result = {
                cons.ECG_SOURCE: source,
                cons.ECG_CHANNEL: channel,
                cons.ECG_SAMPLE_RATE: sample_rate,
                cons.ECG_UNIT: unit,
                cons.ECG_COMMENTS: comments
            }
    
    return result
