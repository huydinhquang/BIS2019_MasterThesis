import streamlit as st
from Controllers.ECGModel import ECG
from Controllers.Configure import Configure
import Controllers.Constants as cons
import Views.DBImport as db_import

config = Configure()
configure = config.get_configure_value()

def load_form():
    return db_import.load_form()

