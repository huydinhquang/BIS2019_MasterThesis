MONGOCONNECTIONSTR = 'mongo'
MONGODB = 'mongodb'
DB_NAME = 'db_name'
COLLECTION_ECG_NAME = 'collection_ecg_name'
COLLECTION_CHANNEL_NAME = 'collection_channel_name'
COLLECTION_RECORD_SET_NAME = 'collection_record_set_name'
COLLECTION_EXPORTING_TEMPLATE_NAME = 'collection_exporting_template_name'
COLLECTION_EXPORTING_REGION_NAME = 'collection_exporting_region_name'

CONFIGURE = 'configure'
CONF_FORMAT_DESCRIPTOR = 'format_descriptor'
CONF_CHANNEL_NAME = 'channel_name'
CONF_FOLDER_IMPORT_RECORD = 'default_folder_import_record'
CONF_FOLDER_IMPORT_RECORD_MASS = 'default_folder_import_record_mass'
CONF_FOLDER_EXPORT_DATA = 'default_folder_export_data'

# ECG Model
ECG_ID_SHORT = '_id'
ECG_CHANNEL = 'channel'
ECG_CREATED_DATE = 'created_date'
ECG_MODIFIED_DATE = 'modified_date'
ECG_SAMPLE_RATE = 'sample_rate'
ECG_SOURCE = 'source'
ECG_TIME = 'time'
ECG_SAMPLE = 'sample'
ECG_ECG = 'ecg'
ECG_FILE_NAME = 'file_name'
ECG_TOTAL_CHANNELS = 'total_channels'
ECG_CHANNEL_TEXT = 'is_channel_from_record'
ECG_UNIT = 'unit'
ECG_COMMENTS = 'comments'
ECG_ID = 'id'
ECG_CHANNEL_INDEX = 'channel_index'

SINGAL_NAME = 'sig_name'
SAMPLING_FREQUENCY = 'fs'
AMPLITUDE_UNIT = 'units'
CONS_OUTPUT_DATA = 'output_data'
CONS_TEMP_STR = 'temp'

CONS_DATE_STR = '$date'
CONS_SET_STR = '$set'
CONS_QUERYIN_STR = '$in'
CONS_QUERYREGEX_STR = '$regex'

# Files collection column name
FILE_ID_SHORT = '_id'
FILE_ECG_FILE_NAME_EXT = 'file_name_ext'
FILE_ECG_ID = 'ecg_id'

# ECG Column Header
HEADER_SOURCE = 'Source'
HEADER_FILENAME = 'File name'
HEADER_ID = 'ID'
HEADER_CHANNEL = 'Channel(s)'
HEADER_CREATED_DATE = 'Created date'
HEADER_MODIFIED_DATE = 'Modified date'
HEADER_SAMPLE_RATE = 'Sample rate'
HEADER_TIME = 'Time'
HEADER_SAMPLES = 'Samples'
HEADER_ECG = 'ECG files'
HEADER_UNIT = 'Unit'
HEADER_CHANNEL_INDEX = 'Channel Index'
HEADER_COMMENTS = 'Comments'

# RecordSet Column Header
HEADER_RECORD_SET = 'RecordSet name'

# Exporting Template Column Header
HEADER_EXP_TEM = 'Exporting template name'
HEADER_TARGET_SAMPLE_RATE = 'Target sample rate'
HEADER_DURATION = 'Duration'

# One Character 
CONS_UNDERSCORE = '_'
CONS_COMMA = ','
CONS_SEMICOLON = ';'

# Global
CONS_UNDEFINED = 'undefined'
CONS_FILE_NAME = 'file_name'
CONS_CHANNEL = 'channel'
CONS_CREATED_DATE = 'created_date'
CONS_MODIFIED_DATE = 'modified_date'
CONS_ID_SHORT = '_id'
CONS_BUTTON_CREATE = 'create_clicked'
CONS_FILE_LIST = 'file_list'
CONS_DIR_LIST = 'dir_list'
CONS_DATE = 'Date'
CONS_METADATA = 'metadata'
CONS_DS_NAME = 'ds_name'
CONS_DS_DATA = 'ds_data'
CONS_DS_METADATA = 'ds_metadata'
CONS_UNIT_MV = 'mV'
CONS_UNIT_V = 'V'
CONS_WFDB = 'wfdb'
CONS_SCIPY = 'scipy'
CONS_ECG = 'ecg'
CONS_SAMPLE_RATE = 'Sample rate'
CONS_COMMENTS = 'Comments'
CONS_ADD_COMMENTS = 'Add any comments here'
CONS_SOURCE_NAME = 'Source name'
CONS_FILE_NAME = 'File name'
CONS_UNIT = 'Unit'
CONS_SAMPLES = 'Samples'
CONS_CHANNELS = 'Channel(s)'
CONS_TIMES = 'Time(s)'
CONS_TOTAL_CHANNELS = 'Total channels'
CONS_IS_UPDATE = 'is_update'
CONS_START_TIME = 'Start time'
CONS_END_TIME = 'End time'
CONS_EXPORTING_REGION = 'exporting_region'

# Record Set
CONS_RECORD_SET_NAME = 'record_set_name'

# Exporting Template
CONS_EXPORTING_TEMPLATE_NAME = 'exporting_template_name'
CONS_TARGET_SAMPLE_RATE = 'target_sample_rate'
CONS_DURATION = 'duration'

# Exporting Region
CONS_EXPORTING_REGION_RECORD_SET_ID = 'record_set_id'
CONS_EXPORTING_REGION_ECG_ID = 'ecg_id'
CONS_EXPORTING_REGION_START_TIME = 'start_time'
CONS_EXPORTING_REGION_END_TIME = 'end_time'
CONS_EXPORTING_REGION_SAMPLE_FROM = 'sample_from'
CONS_EXPORTING_REGION_SAMPLE_TO = 'sample_to'

# Query
CONS_QUERY_FROM = 'from'
CONS_QUERY_LOCALFIELD = 'localField'
CONS_QUERY_FOREIGNFIELD = 'foreignField'
CONS_QUERY_AS = 'as'
CONS_QUERY_LET = 'let'
CONS_QUERY_PIPELINE = 'pipeline'
CONS_QUERY_PATH = 'path'
CONS_QUERY_PRESERVE = 'preserveNullAndEmptyArrays'
CONS_QUERY_MATCH_QUERY = '$match'
CONS_QUERY_LOOKUP_QUERY = '$lookup'
CONS_QUERY_UNWIND_QUERY = '$unwind'
CONS_QUERY_GROUP_QUERY = '$group'
CONS_QUERY_PROJECT_QUERY = '$project'
CONS_QUERY_EXPR_QUERY = '$expr'
CONS_QUERY_AND_QUERY = '$and'
CONS_QUERY_EQ_QUERY = '$eq'
CONS_QUERY_PUSH_QUERY = '$push'

# HDF5 Attribute
CONS_HDF5_DS_SIGNAL = 'dataset_signal'
CONS_HDF5_DS_RECORDSET = 'dataset_recordset'