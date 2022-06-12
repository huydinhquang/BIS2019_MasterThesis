from bson.objectid import ObjectId
import numpy as np
import streamlit as st
import pandas as pd
import Controllers.Constants as cons
import Controllers.Common as common
from Controllers.ExportingTemplateModel import ExportingTemplate
import Scraper as scraper
import Scrapers.ManageData.ManageExportingTemplateScraper as manage_exporting_template_scraper
import Controllers.Helper as helper
from Controllers.Configure import Configure

config = Configure()
configure = config.get_configure_value()

class ManageExportingTemplateProcessor:
    def load_record_data(self, db_result):
        exp_template_col = db_result[cons.COLLECTION_TEMPLATE_EXPORTATION_NAME]
        count = 0
        list_exp_template = []

        data = scraper.find(exp_template_col)

        # Check if there is no imported record in the DB --> If so, return a warning message
        if (data.count() < 1):
            st.warning('There is no item. Please check again!')
            st.stop()
        
        for exp_template in data:
            count = count + 1
            list_exp_template.append(ExportingTemplate(
                exporting_template_name=exp_template[cons.CONS_EXPORTING_TEMPLATE_NAME],
                channel=common.convert_list_to_string(exp_template[cons.CONS_CHANNEL]).upper(),
                target_sample_rate=exp_template[cons.CONS_TARGET_SAMPLE_RATE],
                duration=exp_template[cons.CONS_DURATION],
                created_date=common.convert_time_to_datetime(exp_template[cons.ECG_CREATED_DATE]),
                modified_date=common.convert_time_to_datetime(exp_template[cons.ECG_MODIFIED_DATE]),
                id=str(exp_template[cons.ECG_ID_SHORT])
            ))
            
        header_table = [
            cons.HEADER_EXP_TEM,
            cons.HEADER_TARGET_SAMPLE_RATE,
            cons.HEADER_DURATION,
            cons.HEADER_CHANNEL,
            cons.HEADER_CREATED_DATE,
            cons.HEADER_MODIFIED_DATE,
            cons.HEADER_ID
        ]

        column_names = [
            cons.CONS_EXPORTING_TEMPLATE_NAME,
            cons.CONS_TARGET_SAMPLE_RATE,
            cons.CONS_DURATION,
            cons.CONS_CHANNEL,
            cons.ECG_CREATED_DATE,
            cons.ECG_MODIFIED_DATE,
            cons.ECG_ID
        ]

        # Generate data from list ECG records to table of DataFrame
        df = pd.DataFrame.from_records([vars(s) for s in list_exp_template])
        # Reorder columns of the DataFrame
        df = df.reindex(columns=column_names)
        # Set header names
        df.columns = header_table

        with st.form("exp_template_data_form"):
            st.write('### Full Dataset', df)
            st.info('Total items: ' + str(count))

            selected_indices = st.multiselect('Select rows:', df.index)

            # Every form must have a submit button.
            clicked = st.form_submit_button("Load record")
            if clicked:
                st.session_state.manage_exp_template = True

            if selected_indices:
                selected_rows = df.loc[selected_indices]
                st.write('### Selected Rows', selected_rows)
            else:
                selected_rows = pd.DataFrame()

        # Count number of selected rows
        number_selected_rows = len(selected_rows.values)
        # Only process if any item is selected
        if st.session_state.manage_exp_template and number_selected_rows > 0:
            col1, col2 = st.columns([.1,1])
            with col1:
                edit_clicked = st.button("Edit")                
                
            with col2:
                delete_clicked = st.button("Delete")
                
            if edit_clicked or st.session_state.edit_exp_template:
                st.session_state.edit_exp_template = True
                if number_selected_rows == 1:
                    self.edit_exp_template(exp_template_col, selected_rows)
                else:
                    st.warning("Please select one item to edit at the time!")
            if delete_clicked or st.session_state.delete_exp_template:
                st.session_state.delete_exp_template = True
                st.warning("Are you sure you want to delete the exporting template(s)?")
                confirm_clicked = st.button("Yes")
                if confirm_clicked:
                    self.delete_exp_template(exp_template_col, selected_rows)

    def delete_exp_template(self, exp_template_col, selected_rows):
        count = 0
        for index, row in selected_rows.iterrows():
            # Get exporting template id
            exp_template_id = ObjectId(row[cons.HEADER_ID])
            # Delete the exporting template
            result_exp_template = manage_exporting_template_scraper.delete_exp_template(exp_template_col, cons.FILE_ID_SHORT, exp_template_id)
            # Check if the exporting template is succsessfully deleted
            if result_exp_template > 0:
                count = count + 1
        st.success(f'Delete successfully {count} items! Please refresh the result.')

    def edit_exp_template(self, exp_template_col, selected_rows):
        with st.form("edit_exp_template_form"):
            st.write('### Edit exporting template')
            for index, row in selected_rows.iterrows():
                exp_template_id = ObjectId(row[cons.HEADER_ID])

                # Exporting Template name
                exp_template_name = st.text_input(cons.HEADER_EXP_TEM, value=row[cons.HEADER_EXP_TEM])
                
                # Target sample rate & Duration
                # Provide slider & text to input data
                slider_value, manual_inp_val = st.columns([0.75,0.25])
                with slider_value:
                    val_target_sample_rate = st.slider('Target sample rate slider', 
                                    min_value = 1,
                                    max_value = 2000,
                                    value=500,
                                    step = 1)
                    val_duration = st.slider('Duration slider', 
                                    min_value = 1,
                                    max_value = 60,
                                    value=5,
                                    step = 1)
                with manual_inp_val:
                    target_sample_rate = int(st.number_input('Target sample rate text', value=val_target_sample_rate))
                    duration = int(st.number_input('Duration text', value=val_duration))

                # Channel multi selection
                # Value is defined from the configuration
                # channel = st.multiselect('Channel(s)', options= configure[cons.CHANNEL_NAME], default=None)

            save_clicked = st.form_submit_button("Save")
            if save_clicked:
                new_exp_template_value = ExportingTemplate(
                    exporting_template_name=exp_template_name,
                    target_sample_rate=target_sample_rate,
                    duration=duration,
                    is_update=True
                )

                # Update Exporting Template
                result_exp_template = manage_exporting_template_scraper.update_exp_template(exp_template_col, cons.FILE_ID_SHORT, exp_template_id, new_exp_template_value)
                # Check if the exporting template is succsessfully updated
                if result_exp_template > 0:
                    st.success('Save successfully! Please refresh the result.')

