import streamlit as st
from Processors.ExportDataProcessor import ExportDataProcessor
import Views.ManageChannelView as manage_channel_view
import Views.TemplateExportationView as template_export_view
import Views.ImportSourceView as import_source_view
import Views.ImportSourceMassView as import_source_mass_view
import Views.RecordSetView as record_set_view
import Views.ExportDataView as export_data_view
import Controllers.MongoDBConnection as con
import Scraper as scraper
import Scrapers.ManageChannelScraper as manage_channel_scraper
import Scrapers.TemplateExportationScraper as template_export_scraper
from Controllers.WFDBController import WFDBController
from Controllers.SciPyController import SciPyController
from Processor import Processor
from Processors.ManageChannelProcessor import ManageChannelProcessor
from Processors.RecordSetProcessor import RecordSetProcessor
from Processors.ImportSourceProcessor import ImportSourceProcessor
import Controllers.Constants as cons

st.title('ECG System')

# Initialization
if 'get_data' not in st.session_state:
	st.session_state.get_data = False
if 'extract_anno' not in st.session_state:
	st.session_state.extract_anno = False
if 'load_source_list' not in st.session_state:
	st.session_state.load_source_list = False
if 'filter_source' not in st.session_state:
	st.session_state.filter_source = False
if 'load_channel_list' not in st.session_state:
	st.session_state.load_channel_list = False
if 'generate_channel' not in st.session_state:
	st.session_state.generate_channel = False

processor = Processor()
manage_channel_processor = ManageChannelProcessor()
record_set_processor = RecordSetProcessor()
export_data_processor = ExportDataProcessor()
import_source_processor = ImportSourceProcessor()

def read_property(dir_name, file_list, file_name,format_desc):
    # Read source ecg property    
    if format_desc == 'wfdb':
        processor.add(WFDBController(dir_name, file_name, file_list))
    else:
        processor.add(SciPyController(dir_name, file_name, file_list))
    return processor.get_source_property()

def read_final_property(ecg_property, file_list, file_name):
    # Get final ecg property
    final_ecg_property = import_source_processor.render_property(ecg_property)

    if final_ecg_property:
        import_source = st.button('Import source')
        if import_source:
            # Open MongoDB connection
            db_result = con.connect_mongodb()

            # Save ECG properties
            import_source_processor.save_ecg_property(db_result, file_list, file_name,final_ecg_property)

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
    ("Home page", "Import Source", "Import Source - Mass Import", "Record Set", "Exporting Template", "Export Data")
)

add_selectbox = add_selectbox.lower()
if add_selectbox == "import source":
    dir_name, format_desc, retrieve_clicked = import_source_view.load_form()
    if retrieve_clicked or st.session_state.get_data:
        st.session_state.get_data = True

        # Process to get the list of files when selecting the folder
        file_list, file_name = import_source_processor.process_file(dir_name)

        # Read ECG properties when user selects a source
        ecg_property = read_property(dir_name, file_list, file_name,format_desc.lower())

        # Read Final ECG properties
        if ecg_property:
            read_final_property(ecg_property, file_list,file_name)

    # new_channel, add_clicked, load_list_clicked = manage_channel_view.load_form()

    # if load_list_clicked:
    #     # Open MongoDB connection
    #     my_db, my_main_col, channel_col, record_set_col = con.connect_mongodb()

    #     # Load all channels
    #     manage_channel_processor.load_list_channel(channel_col)
    
    # if add_clicked:
    #     # Open MongoDB connection
    #     my_db, my_main_col, channel_col, record_set_col = con.connect_mongodb()

    #     channel_id = manage_channel_scraper.add_channel(channel_col, new_channel)
    #     if channel_id:
    #         st.success('Added successfully!')
    #     else:
    #         st.warning('Please try again!')

elif add_selectbox == "import source - mass import":
    dir_name, format_desc, retrieve_clicked = import_source_mass_view.load_form()
    if retrieve_clicked or st.session_state.get_data:
        st.session_state.get_data = True

        # Process to get the list of files when selecting the folder
        file_list, file_name = import_source_processor.process_file(dir_name)

        # Read ECG properties when user selects a source
        # ecg_property = read_property(dir_name, file_list, file_name,format_desc.lower())

        # Read Final ECG properties
        # if ecg_property:
        #     read_final_property(ecg_property, file_list,file_name)

elif add_selectbox == "record set":
    load_source_list_clicked = record_set_view.load_form()
    if load_source_list_clicked or st.session_state.load_source_list:
        st.session_state.load_source_list = True

        # Open MongoDB connection
        db_result = con.connect_mongodb()

        # Load result after list channels selection
        record_set_id = record_set_processor.load_source_data(db_result)

        if record_set_id:
            st.success('Added successfully!')

elif add_selectbox == "exporting template":
    form_result = template_export_view.load_form()

    # Retrieve data from the view
    create_clicked = form_result[cons.CONS_BUTTON_CREATE]
    list_channel = form_result[cons.CONS_CHANNEL]
    exp_tem_name = form_result[cons.CONS_EXPORTING_TEMPLATE_NAME]

    if create_clicked and exp_tem_name and len(list_channel) > 0:
        # Open MongoDB connection
        db_result = con.connect_mongodb()
        template_id = template_export_scraper.add_template(db_result[cons.COLLECTION_TEMPLATE_EXPORTATION_NAME], form_result)
        if template_id:
            st.success('Added successfully!')
        else:
            st.warning('Please try again!')

elif add_selectbox == "export data":
    load_data_clicked = export_data_view.load_form()
    if load_data_clicked or st.session_state.extract_anno:
        st.session_state.extract_anno = True

        # Open MongoDB connection
        db_result = con.connect_mongodb()

        # Load result after list channels selection
        record_set_id = export_data_processor.load_data(db_result)