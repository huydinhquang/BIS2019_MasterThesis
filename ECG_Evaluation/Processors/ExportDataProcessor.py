from bson.objectid import ObjectId
import streamlit as st
import pandas as pd
import Controllers.Constants as cons
import Controllers.Common as common
from Controllers.RecordSetModel import RecordSet
from Controllers.ExportingTemplateModel import ExportingTemplate
import Scrapers.ExportDataScraper as export_data_scraper
import Scraper as scraper
from Controllers.ECGModel import ECG
from Controllers.FilesModel import Files
import Controllers.Helper as helper
import os
import Controllers.WFDBHelper as wfdb_helper
import numpy as np
from Controllers.Configure import Configure

config = Configure()
configure = config.get_configure_value()

class ExportDataProcessor:
    def load_channel_list_from_record_set(self, ecg_col, record_set_col, exp_region_col, record_set_id):
        query_data = {
            cons.CONS_QUERY_LOCALFIELD: cons.ECG_SOURCE,
            cons.CONS_QUERY_FOREIGNFIELD: cons.CONS_ID_SHORT,
            cons.CONS_ID_SHORT: record_set_id
        }

        # Append a value to the existing 'from' key 
        helper.add_value(query_data, cons.CONS_QUERY_FROM, ecg_col.name)
        helper.add_value(query_data, cons.CONS_QUERY_FROM, exp_region_col.name)

        # Append a value to the existing 'as' key 
        helper.add_value(query_data, cons.CONS_QUERY_AS, ecg_col.name)
        helper.add_value(query_data, cons.CONS_QUERY_AS, exp_region_col.name)

        result = export_data_scraper.find_channel_list(record_set_col, query_data)
        return result
    
    def load_record_set_data(self, record_set_col):
        count = 0
        list_record_set = []
        # data = scraper.find_by_query(my_main_col, cons.CONS_QUERYREGEX_STR, cons.ECG_SOURCE, source_name)
        record_set_data = scraper.find(record_set_col)
        for record in record_set_data:
            count = count + 1
            list_record_set.append(RecordSet(
                record_set_name=record[cons.CONS_RECORD_SET_NAME],
                created_date=common.convert_time_to_datetime(record[cons.CONS_CREATED_DATE]),
                modified_date=common.convert_time_to_datetime(record[cons.CONS_MODIFIED_DATE]),
                id=str(record[cons.ECG_ID_SHORT])
            ))

        # Check if there is no imported record in the DB --> If so, return a warning message
        if count < 1:
            st.warning('There is no item of RecordSet. Please check again!')
            st.stop()

        header_table = [
            cons.HEADER_RECORD_SET,
            cons.HEADER_CREATED_DATE,
            cons.HEADER_MODIFIED_DATE,
            cons.HEADER_ID
        ]

        column_names = [
            cons.CONS_RECORD_SET_NAME,
            cons.ECG_CREATED_DATE,
            cons.ECG_MODIFIED_DATE,
            cons.ECG_ID
        ]

        # Generate data from list RecordSet to table of DataFrame
        df = pd.DataFrame.from_records([vars(s) for s in list_record_set])
        # Reorder columns of the DataFrame
        df = df.reindex(columns=column_names)
        # Set header names
        df.columns = header_table

        return df, count


    def load_exp_tem_data(self, exp_tem_col):
        # st.session_state.select_row = True
        count = 0
        list_exp_tem_set = []
        # data = scraper.find_by_query(my_main_col, cons.CONS_QUERYREGEX_STR, cons.ECG_SOURCE, source_name)
        record_set_data = scraper.find(exp_tem_col)
        for record in record_set_data:
            count = count + 1
            list_exp_tem_set.append(ExportingTemplate(
                exporting_template_name=record[cons.CONS_EXPORTING_TEMPLATE_NAME],
                channel=common.convert_list_to_string(record[cons.CONS_CHANNEL]),
                target_sample_rate=str(record[cons.CONS_TARGET_SAMPLE_RATE]),
                duration=str(record[cons.CONS_DURATION]),
                created_date=common.convert_time_to_datetime(record[cons.CONS_CREATED_DATE]),
                modified_date=common.convert_time_to_datetime(record[cons.CONS_MODIFIED_DATE]),
                id=str(record[cons.ECG_ID_SHORT])
            ))
            
        # Check if there is no imported record in the DB --> If so, return a warning message
        if count < 1:
            st.warning('There is no item of Exporting Template. Please check again!')
            st.stop()

        header_table = [
            cons.HEADER_EXP_TEM,
            cons.HEADER_CHANNEL,
            cons.HEADER_TARGET_SAMPLE_RATE,
            cons.HEADER_DURATION,
            cons.HEADER_CREATED_DATE,
            cons.HEADER_MODIFIED_DATE,
            cons.HEADER_ID
        ]

        df = pd.DataFrame.from_records([vars(s) for s in list_exp_tem_set])
        df.columns = header_table

        return df, count

    def load_data(self, db_result):
        ecg_col= db_result[cons.COLLECTION_ECG_NAME]
        record_set_col= db_result[cons.COLLECTION_RECORD_SET_NAME]
        exp_tem_col=db_result[cons.COLLECTION_EXPORTING_TEMPLATE_NAME]
        exp_region_col= db_result[cons.COLLECTION_EXPORTING_REGION_NAME]

        # Load full dataset of RecordSet
        df_record_set, count_record_set = self.load_record_set_data(record_set_col)
        st.write('### RecordSet Data', df_record_set)
        st.info('Total items: {}'.format(str(count_record_set)))

        record_set_selected_indices = st.selectbox('Select rows:', df_record_set.index, key=record_set_col.name)
        record_set_selected_rows = df_record_set.loc[record_set_selected_indices]
        st.write('### Selected Rows', record_set_selected_rows)
            
        # Load full dataset of Exporting Template
        df_exp_tem, count_exp_tem = self.load_exp_tem_data(exp_tem_col)
        st.write('### Exporting Template Data', df_exp_tem)
        st.info('Total items: {}'.format(str(count_exp_tem)))
        
        exp_tem_selected_indices = st.selectbox('Select rows:', df_exp_tem.index, key=exp_tem_col.name)
        exp_tem_selected_rows = df_exp_tem.loc[exp_tem_selected_indices]
        st.write('### Selected Rows', exp_tem_selected_rows)

        # Add a 'Generate channel' button
        generate_clicked = st.button('Generate channel')

        if generate_clicked or st.session_state.generate_channel:
            st.session_state.generate_channel = True
            
            # Get RecordSet Id to find related ECG with channels
            record_set_id=ObjectId(record_set_selected_rows[cons.HEADER_ID])
            
            # Query to get list of ECG channels based on RecordSet Id
            result = self.load_channel_list_from_record_set(ecg_col, record_set_col, exp_region_col, record_set_id)
            
            # Nested For Loop
            # Loop of RecordSet because it is a result --> Loop of RecordSet-ecg (here is ecg record) --> Get list of channels
            # Ex: 1 record set has many ecg records, and each ecg record has a collection of channels
            # Get more data with Record Id and file name
            ecg_data = [
                ECG(id=y[cons.CONS_ECG][cons.ECG_ID_SHORT],
                    file_name=y[cons.CONS_ECG][cons.ECG_FILE_NAME],
                    channel=y[cons.CONS_ECG][cons.ECG_CHANNEL],
                    sample_rate=y[cons.CONS_ECG][cons.ECG_SAMPLE_RATE],
                    exporting_region=y[cons.CONS_EXPORTING_REGION])
                for x in result for y in x[ecg_col.name]
            ]

            # Get text of channels based on selected exporting template
            list_channels_str = 'Channel {}'.format(exp_tem_selected_rows[cons.HEADER_CHANNEL])
            
            # Retrieve list of channels from Exporting Template
            list_channels = common.convert_string_to_list(exp_tem_selected_rows[cons.HEADER_CHANNEL], cons.CONS_SEMICOLON, True)

            with st.form("extract_data_form"):
                # Widgets will be genrated by the number of ECG records
                # This is used for mapping channel between ECG record and Exporting template
                for x in ecg_data:
                    st.write('{} from selected exporting template'.format(list_channels_str))
                    # Try to map channels with the common names, which are defined in the exporting template (Ex: I, II, III)
                    list_existed_channels = helper.get_list_existed_channels(list_channels, x.channel)
                    if list_existed_channels:
                        st.multiselect(label='Record: {}'.format(x.file_name), options=x.channel, default=list_existed_channels, key=str(x.id))
                    else:
                        st.multiselect(label='Record: {}'.format(x.file_name), options=x.channel, key=str(x.id))

                folder_download = st.text_input(label='Downloadable folder:', value=configure[cons.CONF_FOLDER_EXPORT_DATA])

                extract_entire = st.checkbox('Extract entire record(s)')

                # Every form must have a submit button.
                extract_clicked = st.form_submit_button("Extract data")
                if extract_clicked:
                    self.extract_data(db_result,ecg_data, folder_download,extract_entire,record_set_selected_rows,exp_tem_selected_rows, list_channels)

    def resample_signal_by_slice(self, record:ECG, ecg_property:ECG, duration, list_channels, target_sample_rate):
        # Create a new matrix to store resampled signal by record
        dataset_signal = []
        dataset_record = []
        
        # Calculate total length of the samples
        len_total_samples = len(ecg_property.sample)

        # Calculate the new length of the samples with the duration in the exporting template
        step = ecg_property.sample_rate * duration

        # Calculate number of slices (the total number samples divided by the step)
        number_slice = len_total_samples / step
        
        # Calculate to get the list of array containing ECG signal data by with slice of the step
        # Ex: [[0, 1, 2, ..., 9], [10, 11, 12, ..., 19], ..., [50, 51, 52, ..., 59]] - 5 slices with step: 10
        result_list = [ ecg_property.sample[int(y):int(y)+step] for y in np.arange(number_slice)*step ]
        
        # Check the length of the last slice
        # Round up 'number_slice' to the next integer
        number_slice_round_up = np.ceil(number_slice)

        # If the last slice does not have enough samples (Ex: 5200 samples instead of 10.000 samples)
        # Add '0' to ensure the last slice will have the same length of samples with the others of the other arrays
        if number_slice_round_up - number_slice > 0:
            # Count the missing number of samples to fill up the length
            missing_len_last_slice = step - len(result_list[-1])
            # Create an empty list for later use
            empty_list = []
            # Add a list of zero to the created list based on the number of selected channels in the Exporting Template
            # Result: [0. 0.] if there are 2 channels. The channels are dynamic, so the result can be different.
            list_append_zero = np.pad(empty_list, (0, len(list_channels)), 'constant')
            # Extend more the missing number of samples to the last slice.
            ########################
            # 0: No item is added to the beginning of the result_list
            # missing_len_last_slice: Number of items is added to the end of the result_list
            # 0: No item is added to the left of the dimension (array)
            # 0: No item is added to the right of the dimension (array)
            ########################
            result_list[-1] = np.pad(result_list[-1], ((0, missing_len_last_slice), (0, 0)), constant_values=list_append_zero)

        # Loop the slice of each record, which is divided by the duration
        for slice in result_list:
            # Get total number of channels in an ECG record
            number_channel = slice.shape[1]
            # Create a new list for each channel array (signal data)
            list_channels_signal = np.array_split(slice, number_channel, axis=1)
            # Create a new matrix to store resampled signal by channel
            list_resampled_signal = []
            for idx, signal in enumerate(list_channels_signal):
                # Calculate the new data point as the resampling process
                resampled_signal = wfdb_helper.resampling_data(signal, target_sample_rate, ecg_property.sample_rate)
                # Append the matrix based on the sequence 
                list_resampled_signal.append(resampled_signal)
                # Visualize each slice of the record (this can reduce the performance)
                # wfdb_helper.visualize_chart(x.file_name, current_channel_name, signal, ecg_property.sample_rate, resampled_signal, target_sample_rate)
            dataset_signal.append(list_resampled_signal)
            dataset_record.append(record.file_name)
        return dataset_signal, dataset_record
    

    def resample_entire_record(self, ecg_data:list[ECG], list_files, duration, list_channels, target_sample_rate):
        # Create a new matrix to store resampled signal by record
        dataset_signal = []
        dataset_record = []
        for x in ecg_data:
            # Get downloaded location of the ECG record
            download_location = helper.get_folder_download(x, list_files)

            # Read the ECG record by the limited channels, which are filtered by the exporting template
            # The channels are accessed by WFDB helper with channel index
            ecg_property:ECG = wfdb_helper.get_record_property_with_condition(
                dir_name=download_location, 
                file_name=x.file_name, 
                channel_target=x.channel_index)

            result_signal, result_record = self.resample_signal_by_slice(x, ecg_property, duration, list_channels, target_sample_rate)
            dataset_signal.append(result_signal)
            dataset_record.append(result_record)

        return dataset_signal, dataset_record


    def resample_target_segment(self, ecg_data:list[ECG], list_files, duration, list_channels, target_sample_rate):
        # Create a new matrix to store resampled signal by record
        dataset_signal = []
        dataset_record = []
        for x in ecg_data:
            # Get downloaded location of the ECG record
            download_location = helper.get_folder_download(x, list_files)

            for r in x.exporting_region:
                sample_from=r[cons.CONS_EXPORTING_REGION_SAMPLE_FROM]
                sample_to=r[cons.CONS_EXPORTING_REGION_SAMPLE_TO]
                ecg_property: ECG = wfdb_helper.get_record_property_with_condition(
                    dir_name=download_location, 
                    file_name=x.file_name,
                    sample_from=sample_from, 
                    sample_to=sample_to, 
                    channel_target=x.channel_index)

                # Calculate number of slices (the total number samples divided by the step)
                result_signal, result_record = self.resample_signal_by_slice(x, ecg_property, duration, list_channels, target_sample_rate)

                dataset_signal.append(result_signal)
                dataset_record.append(result_record)

        return dataset_signal, dataset_record

    def extract_data(self,db_result, ecg_data:list[ECG], folder_download,extract_entire,record_set,exp_tem, list_channels):
        db= db_result[cons.DB_NAME]
        # Loop record in selected RecordSet
        for x in ecg_data:
            selected_channel = st.session_state[x.id]
            list_channels_index = helper.get_list_index(selected_channel, x.channel)
            x.channel_index=list_channels_index

        list_selected_ecg_id = [x.id for x in ecg_data]

        # Search by list of ECG Id to retrieve ECG files
        list_files:list[Files] = export_data_scraper.retrieve_ecg_files(db, list_selected_ecg_id)

        # Download and store the ECG files from MongoDB to local
        # Create a folder for each file name to store all related ECG files (Ex: *.dat, *.hea, *.xyz)
        for x in list_files:
            # file_name = helper.get_file_name(x.file_name)
            download_location = os.path.join(folder_download, f'{x.ecg_id}{cons.CONS_UNDERSCORE}{x.file_name}{cons.CONS_UNDERSCORE}{cons.CONS_TEMP_STR}')
            helper.write_file(download_location, x.file_name_ext, x.output_data)
            x.folder_download = download_location

        # Retrieve Target sample rate, Duration, list of channels from Exporting Template
        target_sample_rate = int(exp_tem[cons.HEADER_TARGET_SAMPLE_RATE])
        duration = int(exp_tem[cons.HEADER_DURATION])

        # Resample signal process
        if extract_entire:
            dataset_signal, dataset_record = self.resample_entire_record(ecg_data, list_files, duration, list_channels, target_sample_rate)
        else:
            dataset_signal, dataset_record = self.resample_target_segment(ecg_data, list_files, duration, list_channels, target_sample_rate)
        
        # Retrieve record set name from RecordSet
        record_set_name = record_set[cons.HEADER_RECORD_SET]
        # Get current date time in string
        current_time = common.convert_current_time_to_str()
        # Build file name for the output
        file_name = '{}_{}.h5'.format(record_set_name,current_time)
        
        ### Build metadata ###
        # For dataset signal
        metadata_signal = {}
        metadata_signal[cons.CONS_DATE] = current_time
        metadata_signal[cons.HEADER_CHANNEL] = exp_tem[cons.HEADER_CHANNEL]
        # For dataset recordset
        metadata_record_set = {}
        metadata_record_set[cons.CONS_DATE] = current_time
        metadata_record_set[cons.HEADER_SAMPLE_RATE] = target_sample_rate
        metadata_record_set[cons.HEADER_TIME] = duration
        metadata_record_set[cons.HEADER_CHANNEL] = exp_tem[cons.HEADER_CHANNEL]
        ### --- ###

        # Merge the resampled signal data of each record into only one array to output final data for HDF5 file format
        # Ex:
        # R1: [[[-0.1905, -0.4675 ], [-0.573, -0.8115 ]], [[-0.468, -0.3585 ], [-0.8145, -0.7735 ]]]
        # R2: [[[-0.145, 0.52], [-0.065, 0.195 ]], [[-0.535, 0.405 ], [-0.05, 0.285 ]]]
        # R3: [[[-0.2445, 0.1275], [-0.229, -0.147]], [[-0.117, -0.043], [-0.151, -0.046]]]
        # Result: [[[-0.1905, -0.4675], [-0.573, -0.8115]], [[-0.468, -0.3585], [-0.8145, -0.7735]],
        #           [[-0.145, 0.52], [-0.065, 0.195]], [[-0.535, 0.405], [-0.05, 0.285]],
        #           [[-0.2445, 0.1275], [-0.229, -0.147]], [[-0.117, -0.043], [-0.151, -0.046]]]
        dataset_signal = helper.merge_array_from_list(dataset_signal)
        
        # Concatenate the record name into only one array (Use for 1D dimension)
        # Ex:
        # R1: ['s0022lre', 's0022lre']
        # R2: ['100', '100']
        # R3: ['xyz', 'xyz']
        # Result: ['s0022lre', 's0022lre', '100', '100', 'xyz', 'xyz']
        dataset_record = helper.concatenate_array_from_list(dataset_record)

        list_dataset = []
        list_dataset.extend([{
            cons.CONS_DS_NAME: cons.CONS_HDF5_DS_SIGNAL,
            cons.CONS_DS_DATA: dataset_signal,
            cons.CONS_DS_METADATA: metadata_signal
            },
            {
            cons.CONS_DS_NAME: cons.CONS_HDF5_DS_RECORDSET,
            cons.CONS_DS_DATA: dataset_record,
            cons.CONS_DS_METADATA: metadata_record_set
            }
        ])

        # Write signal data into the hfd5 file
        helper.create_hdf5(folder_download, file_name, list_dataset)

        st.success('Extract completed!')
