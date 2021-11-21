import streamlit as st
import Views.DBImport as db_import
import Views.AnnotationExtractor as ann_extract
import Controllers.MongoDBConnection as con
import Scraper as scraper
from Controllers.WFDBController import WFDBController
from Controllers.SciPyController import SciPyController
from Processor import Processor

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

processor = Processor()

def read_property(dir_name, file_name):
    # Read source ecg property    
    processor.add(WFDBController(dir_name, file_name))
    return processor.get_source_property()
    
def read_final_property(ecg_property):
    # Get final ecg property
    final_ecg_property = processor.render_property(ecg_property)

    if final_ecg_property:
        import_source = st.button('Import source')
        if import_source:
            # Open MongoDB connection
            my_db, my_main_col = con.connect_mongodb()

            list_file_id = []
            for item in file_list:
                # Save ECG file to MongoDB
                file_id = scraper.save_ecg_file(my_db, item[1], item[0])
                if file_id:
                    list_file_id.append([file_id])
            ecg_id = scraper.save_ecg_property(my_main_col, final_ecg_property, list_file_id)
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
        file_list, file_name = processor.process_file(dir_name)

        # Read ECG properties when user selects a source
        ecg_property = read_property(dir_name, file_name)

        # Read Final ECG properties
        read_final_property(ecg_property)
elif add_selectbox.lower() == "extract annotations":
    list_channel, sample_rate, export_unit, clicked = ann_extract.load_form()
    if clicked or st.session_state.select_row:
        st.session_state.select_row = True

        # Open MongoDB connection
        my_db, my_main_col = con.connect_mongodb()

        # Load result after list channels selection
        processor.load_source_data(my_main_col, list_channel)
