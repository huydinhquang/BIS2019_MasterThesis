import streamlit as st
from ECG_Evaluation.Controllers.FilesModel import Files
from Processors.ExportDataProcessor import ExportDataProcessor
import Views.TemplateExportationView as template_export_view
import Views.ImportRecordView as import_record_view
import Views.ImportRecordMassView as import_record_mass_view
import Views.RecordSetView as record_set_view
import Views.ExportDataView as export_data_view
import Views.ManageRecordView as manage_record_view
import Controllers.MongoDBConnection as con
import Scrapers.TemplateExportationScraper as template_export_scraper
from Processors.RecordSetProcessor import RecordSetProcessor
from Processors.ImportRecordProcessor import ImportRecordProcessor
from Processors.ImportRecordMassProcessor import ImportRecordMassProcessor
from Processors.ManageData.ManageRecordProcessor import ManageRecordProcessor
import Controllers.Constants as cons
import Controllers.WFDBHelper as wfdb_helper

st.title('ECG System')

# Initialization
if 'get_data' not in st.session_state:
	st.session_state.get_data = False
if 'extract_anno' not in st.session_state:
	st.session_state.extract_anno = False
if 'load_record_list' not in st.session_state:
	st.session_state.load_record_list = False
if 'filter_record' not in st.session_state:
	st.session_state.filter_record = False
if 'load_channel_list' not in st.session_state:
	st.session_state.load_channel_list = False
if 'manage_record' not in st.session_state:
	st.session_state.manage_record = False

record_set_processor = RecordSetProcessor()
export_data_processor = ExportDataProcessor()
import_record_processor = ImportRecordProcessor()
import_record_mass_processor = ImportRecordMassProcessor()
manage_record_processor = ManageRecordProcessor()


def read_final_property(ecg_property, dir_name, file_path, file_name_ext, file_name):
    # Get final ecg property
    final_ecg_property = import_record_processor.render_property(ecg_property)

    if final_ecg_property:
        import_record = st.button('Import record')
        if import_record:
            # Open MongoDB connection
            db_result = con.connect_mongodb()

            # Save ECG properties
            import_record_processor.save_ecg_property(db_result, dir_name, file_path, file_name_ext, file_name,final_ecg_property)

main_selectbox = st.sidebar.selectbox(
    "Task",
    ("Home page", "Import Record", "Import Record - Mass Import", "Record Set", "Exporting Template", "Export Data", "Manage Data")
)

main_selectbox = main_selectbox.lower()
if main_selectbox == "import record":
    dir_name, format_desc, retrieve_clicked = import_record_view.load_form()
    if retrieve_clicked or st.session_state.get_data:
        st.session_state.get_data = True

        # Process to get the list of files when selecting the folder
        file_list:list[Files] = import_record_processor.process_file(dir_name)

        if file_list and len(file_list) > 1:
            st.warning(f'There are more than one record. Please use \'Import Record - Mass Import\' function')
        else:
            for ecg_record in file_list:
                # Read ECG properties when user selects a record
                ecg_property = wfdb_helper.read_property(dir_name, ecg_record.file_path, ecg_record.file_name,format_desc.lower())

                # Read Final ECG properties
                if ecg_property:
                    read_final_property(ecg_property, dir_name, ecg_record.file_path, ecg_record.file_name_ext, ecg_record.file_name)
        
elif main_selectbox == "import record - mass import":
    dir_name, format_desc, retrieve_clicked = import_record_mass_view.load_form()
    if retrieve_clicked or st.session_state.get_data:
        st.session_state.get_data = True

        # Process to get the list of files when selecting the folder
        file_list:list[Files] = import_record_processor.process_file(dir_name)

        if file_list:
            # Display the total of records can be found from the file path
            st.info(f'Number of records found: {len(file_list)}')

            list_ecg_attributes = import_record_mass_view.render_property()
            if list_ecg_attributes:
                # Open MongoDB connection
                db_result = con.connect_mongodb()

                # Save ECG properties
                # Read ECG properties when user selects a record
                import_record_mass_processor.save_ecg_property_mass(db_result, dir_name, file_list, format_desc, list_ecg_attributes)

elif main_selectbox == "record set":
    load_record_list_clicked = record_set_view.load_form()
    if load_record_list_clicked or st.session_state.load_record_list:
        st.session_state.load_record_list = True

        # Open MongoDB connection
        db_result = con.connect_mongodb()

        # Load result after list channels selection
        record_set_id = record_set_processor.load_record_data(db_result)

        if record_set_id:
            st.success('Added successfully!')

elif main_selectbox == "exporting template":
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

elif main_selectbox == "export data":
    load_data_clicked = export_data_view.load_form()
    if load_data_clicked or st.session_state.extract_anno:
        st.session_state.extract_anno = True

        # Open MongoDB connection
        db_result = con.connect_mongodb()

        # Load result after list channels selection
        record_set_id = export_data_processor.load_data(db_result)

elif main_selectbox == "manage data":
    manage_data_selectbox = st.sidebar.selectbox(
        "Manage Data",
        ("Record", "Record Set", "Exporting Template")
    )

    manage_data_selectbox = manage_data_selectbox.lower()
    if manage_data_selectbox == "record":
        load_data_clicked = manage_record_view.load_form()
        if load_data_clicked or st.session_state.manage_record:
            st.session_state.manage_record = True
            
            # Open MongoDB connection
            db_result = con.connect_mongodb()

            # Load all records, which are imported into DB
            record_id = manage_record_processor.load_record_data(db_result)