from pymongo import common
import streamlit as st
import Views.DBImport as db_import
import Views.AnnotationExtractor as ann_extract
import Controllers.MongoDBConnection as con
import Processor as processor
import Scraper as scraper
import os
import numpy as np

st.title('Test System')

# Initialization
if 'get_data' not in st.session_state:
	st.session_state.get_data = False
if 'get_select_source' not in st.session_state:
	st.session_state.get_select_source = False
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
        st.success('Imported successfully!')

def read_property(file_list, file_name, dir_name):
    # Read source ecg property
    ecg_property = processor.get_source_property(file_name, dir_name)
    
    # Get final ecg property
    final_ecg_property = processor.render_property(ecg_property)

    if final_ecg_property:
        import_source = st.button('Import source')
        if import_source:
            # Create folder and write each channel from the source
            processor.write_channel(final_ecg_property, file_name, dir_name)

            import_data(final_ecg_property, file_list)


add_selectbox = st.sidebar.selectbox(
    "Task",
    ("Home page", "Import source", "Extract annotations")
)

if add_selectbox.lower() == "import source":
    dir_name = db_import.load_form()
    clicked = st.button('Get file')
    if clicked or st.session_state.get_data:
        st.session_state.get_data = True

        # Process to get the list of files when selecting the folder
        file_list, file_name = process_file(dir_name)

        # Read ECG properties when user selects a source
        read_property(file_list, file_name, dir_name)
elif add_selectbox.lower() == "extract annotations":
    list_channel = ann_extract.load_form()
    
    # Open MongoDB connection
    my_db = con.connect_mongodb()
    my_col = con.connect_mongo_collectiondb()

    processor.load_source_data(my_col, list_channel)
    


