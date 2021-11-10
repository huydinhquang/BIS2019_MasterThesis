from pymongo import common
import streamlit as st
import Views.DBImport as db_import
import Views.AnnotationExtractor as ann_extract
import Controllers.MongoDBConnection as con
import Processor as processor
import Scraper as scraper
import os
import numpy as np
from Controllers.ECGModel import ECG

st.title('Test System')

# Initialization
if 'get_data' not in st.session_state:
	st.session_state.get_data = False
# if 'filter_source' not in st.session_state:
# 	st.session_state.filter_source = False
if 'select_row' not in st.session_state:
	st.session_state.select_row = False
# if 'connect_dba' not in st.session_state:
# 	st.session_state.connect_dba = False

# def connect_db():
#     if not st.session_state.connect_dba:
#         st.session_state.connect_dba = True
#         # Open MongoDB connection
#         return con.connect_mongodb(), con.connect_mongo_collectiondb()

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
        st.error('Cannot read source folder!')
        st.stop()
    return np.concatenate((file_list, dir_list), axis=1), file_name

def import_data(my_db, my_col, final_ecg_property, file_list):
    list_file_id = []
    for item in file_list:
        # Save ECG file to MongoDB
        file_id = scraper.save_ecg_file(my_db, item[1], item[0])
        if file_id:
            list_file_id.append([file_id])
    ecg_id = scraper.save_ecg_property(my_col, final_ecg_property, list_file_id, False)
    if ecg_id:
        print('ecg_sub_id: ' + str(ecg_id))
        return ecg_id

def read_property(file_name, dir_name):
    # Read source ecg property
    return processor.get_source_property(file_name, dir_name)
    
def read_final_property(file_name, dir_name, ecg_property):
    # Get final ecg property
    final_ecg_property = processor.render_property(ecg_property)

    if final_ecg_property:
        import_source = st.button('Import source')
        if import_source:
            # Create folder and write each channel from the source
            list_sub_channel_folder = processor.write_channel(final_ecg_property, file_name, dir_name)

            # Open MongoDB connection
            my_db, my_main_col, my_channel_col = con.connect_mongodb()

            # Insert separated ECG channels to MongoDB
            list_ecg_sub_id = []
            for item in list_sub_channel_folder:
                # Process to get the list of files when selecting the folder
                file_sub_list, file_sub_name = process_file(item)

                # Read ECG properties for each ecg channel folder
                ecg_sub_property = read_property(file_sub_name, item)
                ecg_sub_property.source = final_ecg_property.source
                ecg_sub_id = import_data(my_db, my_channel_col, ecg_sub_property, file_sub_list)
                if ecg_sub_id:
                    list_ecg_sub_id.append([ecg_sub_id])
            
            # Insert ECG Main (source) to MongoDB
            ecg_id = scraper.save_ecg_property(my_main_col, final_ecg_property, list_ecg_sub_id, True)
            if ecg_id:
                print('ecg_id: ' + str(ecg_id))
                st.success('Imported successfully!')


add_selectbox = st.sidebar.selectbox(
    "Task",
    ("Home page", "Import source", "Extract annotations")
)

if add_selectbox.lower() == "import source":
    dir_name, clicked = db_import.load_form()
    if clicked or st.session_state.get_data:
        st.session_state.get_data = True

        # Process to get the list of files when selecting the folder
        file_list, file_name = process_file(dir_name)

        # Read ECG properties when user selects a source
        ecg_property = read_property(file_name, dir_name)

        # Read Final ECG properties
        read_final_property(file_name, dir_name, ecg_property)

elif add_selectbox.lower() == "extract annotations":
    list_channel, sample_rate, export_unit, clicked = ann_extract.load_form()
    if clicked:
        # st.session_state.filter_source = True

        # Open MongoDB connection
        my_db, my_main_col, my_channel_col = con.connect_mongodb()

        # Load result after list channels selection
        processor.load_source_data(my_channel_col, list_channel)
    


