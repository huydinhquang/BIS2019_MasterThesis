import streamlit as st
from ECG_Evaluation.Controllers.FilesModel import Files
from Processors.ExportDataProcessor import ExportDataProcessor
import Views.TemplateExportationView as template_export_view
import Views.ImportSourceView as import_source_view
import Views.ImportSourceMassView as import_source_mass_view
import Views.RecordSetView as record_set_view
import Views.ExportDataView as export_data_view
import Controllers.MongoDBConnection as con
import Scrapers.TemplateExportationScraper as template_export_scraper
# from Controllers.WFDBController import WFDBController
# from Controllers.SciPyController import SciPyController
# from Processor import Processor
from Processors.ManageChannelProcessor import ManageChannelProcessor
from Processors.RecordSetProcessor import RecordSetProcessor
from Processors.ImportSourceProcessor import ImportSourceProcessor
from Processors.ImportSourceMassProcessor import ImportSourceMassProcessor
import Controllers.Constants as cons
import Controllers.WFDBHelper as wfdb_helper

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

# processor = Processor()
manage_channel_processor = ManageChannelProcessor()
record_set_processor = RecordSetProcessor()
export_data_processor = ExportDataProcessor()
import_source_processor = ImportSourceProcessor()
import_source_mass_processor = ImportSourceMassProcessor()


def read_final_property(ecg_property, dir_name, file_path, file_name_ext, file_name):
    # Get final ecg property
    final_ecg_property = import_source_processor.render_property(ecg_property)

    if final_ecg_property:
        import_source = st.button('Import source')
        if import_source:
            # Open MongoDB connection
            db_result = con.connect_mongodb()

            # Save ECG properties
            import_source_processor.save_ecg_property(db_result, dir_name, file_path, file_name_ext, file_name,final_ecg_property)

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
        file_list:list[Files] = import_source_processor.process_file(dir_name)

        if file_list and len(file_list) > 1:
            st.warning(f'There are more than one source. Please use \'Import Source - Mass Import\' function')
        else:
            for ecg_record in file_list:
                # Read ECG properties when user selects a source
                ecg_property = wfdb_helper.read_property(dir_name, ecg_record.file_path, ecg_record.file_name,format_desc.lower())

                # Read Final ECG properties
                if ecg_property:
                    read_final_property(ecg_property, dir_name, ecg_record.file_path, ecg_record.file_name_ext, ecg_record.file_name)
            
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
        file_list:list[Files] = import_source_processor.process_file(dir_name)

        if file_list:
            # Display the total of sources can be found from the file path
            st.info(f'Number of sources found: {len(file_list)}')

            list_ecg_attributes = import_source_mass_view.render_property()
            if list_ecg_attributes:
                # Open MongoDB connection
                db_result = con.connect_mongodb()

                # Save ECG properties
                # Read ECG properties when user selects a source
                import_source_mass_processor.save_ecg_property_mass(db_result, dir_name, file_list, format_desc, list_ecg_attributes)

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