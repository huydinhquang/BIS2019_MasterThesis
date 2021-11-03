from pymongo import common
import streamlit as st
import Views.DBImport as db_import
import Controllers.MongoDBConnection as con
import Processor as processor
import Scraper as scraper
import os
import numpy as np
import Controllers.Common as common

st.title('Test System')

def process_file(dir_name):
    file_list=[]
    dir_list=[]
    file_name=None
    for root, dirs, files in os.walk(dir_name):
        for file in files:
            # file_name=os.path.join(root, file)
            file_list.append([file])
            dir_list.append([dir_name + '/' + file])
            if not file_name:
                file_name = file.split(".")[0]
    if not file_list or not dir_list:
        st.write('Cannot read source folder!')
        st.stop()
    return np.concatenate((file_list, dir_list), axis=1), file_name

def import_data(final_ecg_property, file_list):
    # Open MongoDB connection
    my_db = con.connect_mongodb()
    my_col = con.connect_mongo_collectiondb()

    list_file_id = []
    for item in file_list:
        # Save ECG file to MongoDB
        file_id = scraper.save_ecg_file(my_db, item[1], item[0])
        if file_id:
            list_file_id.append([file_id])
    ecg_id = scraper.save_ecg_property(my_col, final_ecg_property, list_file_id)
    if ecg_id:
        print('ecg_id: ' + str(ecg_id))
        common.render_text_success('Imported successfully!')

def read_property(file_list, file_name, dir_name):
    ecg_property = processor.get_source_property(file_name, dir_name)
    # st.write(ecg_property.channel)
    if not ecg_property.channel:
        st.write('Cannot read source property!')
        st.stop()

    final_ecg_property = processor.render_property(ecg_property)

    import_source = st.button('Import source')
    if import_source:
        import_data(final_ecg_property, file_list)

# Initialization
if 'get_data' not in st.session_state:
	st.session_state.get_data = False

dir_name = db_import.load_form()
clicked = st.button('Get file')
if clicked or st.session_state.get_data:
    st.session_state.get_data = True

    # Process to get the list of files when selecting the folder
    file_list, file_name = process_file(dir_name)

    # Read ECG properties when user selects a source
    read_property(file_list, file_name, dir_name)
