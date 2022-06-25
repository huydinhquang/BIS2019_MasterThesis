import Controllers.Constants as cons
import Scrapers.ExportingTemplateScraper as exporting_template_scraper
import streamlit as st

class ExportingTemplateProcessor:
    def save_exporting_template(self, exporting_template_col, form_result):
        # Retrieve data from the view
        create_clicked = form_result[cons.CONS_BUTTON_CREATE]
        list_channel = form_result[cons.CONS_CHANNEL]
        exp_tem_name = form_result[cons.CONS_EXPORTING_TEMPLATE_NAME]

        if create_clicked and exp_tem_name and len(list_channel) > 0:
            exporting_template_id = exporting_template_scraper.add_exporting_template(exporting_template_col, form_result)
            if exporting_template_id:
                st.success('Added successfully!')
            else:
                st.warning('Please try again!')