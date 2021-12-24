import streamlit as st
import Views.DBImport as db_import
import Views.AnnotationExtractor as ann_extract
import Views.ResampleSignal as resample_signal
import Controllers.MongoDBConnection as con
import Scraper as scraper
from Controllers.WFDBController import WFDBController
from Controllers.SciPyController import SciPyController
from Processor import Processor

st.title('Test System')

# Initialization
if 'get_data' not in st.session_state:
	st.session_state.get_data = False
if 'resample_signal' not in st.session_state:
	st.session_state.resample_signal = False
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

def read_property(dir_name, file_name, file_list, format_desc):
    # Read source ecg property    
    if format_desc == 'wfdb':
        processor.add(WFDBController(dir_name, file_name))
    else:
        processor.add(SciPyController(dir_name, file_name, file_list))
    return processor.get_source_property()

# def read_property_constraint(dir_name, file_name, file_list, format_desc, signal_start, signal_end, channel_target):
#     # Read source ecg property    
#     if format_desc == 'wfdb':
#         processor.add(WFDBController(dir_name, file_name, signal_start, signal_end, channel_target))
#     else:
#         processor.add(SciPyController(dir_name, file_name, file_list))
#     return processor.get_source_property_constraint()

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

def read_downloaded_property(ecg_property):
    processor.render_property(ecg_property)
    sample_rate_val = 1
    if ecg_property.sample_rate:
        sample_rate_val = ecg_property.sample_rate
    sample_rate = st.sidebar.number_input('Sample rate', min_value=0,max_value=10000,value=sample_rate_val)
    signal_start = st.sidebar.number_input('Time start', min_value=0,max_value=10000,value=10)
    signal_end = st.sidebar.number_input('Time end', min_value=0,max_value=10000,value=250)
    interpolate_signal = st.sidebar.button('Interpolate visualization')
    if interpolate_signal:
        st.write('### Interpolate visualization')
        # ecg_property = read_property(dir_name, file_name, file_list, format_desc.lower(), signal_start, signal_end, 10)
        processor.visualize_chart(ecg_property.sample[:,0], sample_rate, ecg_property.sample_rate)

add_selectbox = st.sidebar.selectbox(
    "Task",
    ("Home page", "Import source", "Extract annotations", "Resample signal")
)

add_selectbox = add_selectbox.lower()
if add_selectbox == "import source":
    dir_name, format_desc, clicked = db_import.load_form()
    if clicked or st.session_state.get_data:
        st.session_state.get_data = True

        # Process to get the list of files when selecting the folder
        file_list, file_name = processor.process_file(dir_name)

        # Read ECG properties when user selects a source
        ecg_property = read_property(dir_name, file_name, file_list, format_desc.lower())

        # Read Final ECG properties
        if ecg_property:
            read_final_property(ecg_property)
elif add_selectbox == "extract annotations":
    # list_channel, sample_rate, export_unit, clicked = ann_extract.load_form()
    list_channel, clicked = ann_extract.load_form()
    if clicked or st.session_state.select_row:
        st.session_state.select_row = True

        # Open MongoDB connection
        my_db, my_main_col = con.connect_mongodb()

        # Load result after list channels selection
        processor.load_source_data(my_main_col, list_channel)
elif add_selectbox == "resample signal":
    dir_name, format_desc, clicked = resample_signal.load_form()
    if clicked or st.session_state.resample_signal:
        st.session_state.resample_signal = True

        # Process to get the list of files when selecting the folder
        file_list, file_name = processor.process_file(dir_name)

        # Read ECG properties when user selects a source
        ecg_property = read_property(dir_name, file_name, file_list, format_desc.lower())

        # Read ECG properties
        if ecg_property:
            read_downloaded_property(ecg_property)