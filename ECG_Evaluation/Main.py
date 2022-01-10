import streamlit as st
import Views.DBImport as db_import
import Views.DownloadChannel as download_channel
import Views.ExtractAnnotations as extract_anno
import Controllers.MongoDBConnection as con
import Scraper as scraper
from Controllers.WFDBController import WFDBController
from Controllers.SciPyController import SciPyController
from Processor import Processor

st.title('ECG System')

# Initialization
if 'get_data' not in st.session_state:
	st.session_state.get_data = False
if 'extract_anno' not in st.session_state:
	st.session_state.extract_anno = False
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
        processor.add(WFDBController(dir_name, file_name, file_list))
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

            # Save ECG properties
            ecg_id = scraper.save_ecg_property(my_main_col, final_ecg_property)
            if ecg_id:
                list_file_id = []
                for item in file_list:
                    # Save ECG file to MongoDB
                    file_id = scraper.save_ecg_file(my_db, item[1], item[0], ecg_id, final_ecg_property)
                    if file_id:
                        list_file_id.append([file_id])
                if len(list_file_id) == final_ecg_property.ecg:
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
    ("Home page", "Import source", "Download Channel", "Extract annotations")
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
elif add_selectbox == "download channel":
    # list_channel, sample_rate, export_unit, clicked = download_channel.load_form()
    list_channel, clicked = download_channel.load_form()
    if clicked or st.session_state.select_row:
        if len(list_channel) > 0:
            st.session_state.select_row = True

            # Open MongoDB connection
            my_db, my_main_col = con.connect_mongodb()

            # Load result after list channels selection
            processor.load_source_data(my_db, my_main_col, list_channel)
        else:
            st.sidebar.warning('Please select channel(s)!')
elif add_selectbox == "extract annotations":
    dir_name, clicked = extract_anno.load_form()
    if clicked or st.session_state.extract_anno:
        st.session_state.extract_anno = True

        # Process to get the list of files when selecting the folder
        file_list = processor.process_folder(dir_name)

        # Read ECG properties when user selects a source
        # ecg_property = read_property(dir_name, file_name, file_list, format_desc.lower())

        processor.load_download_source(file_list)
        # Read ECG properties
        # if ecg_property:
        #     read_downloaded_property(ecg_property)