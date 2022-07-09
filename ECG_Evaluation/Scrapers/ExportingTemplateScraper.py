import Controllers.Common as common
import Controllers.Constants as cons
from ECG_Evaluation.Controllers.ExportingTemplateModel import ExportingTemplate

def add_exporting_template(exporting_template_col, values:ExportingTemplate):
    current_date = common.get_current_date()
    new_exporting_template_json = {
        cons.CONS_EXPORTING_TEMPLATE_NAME: values[cons.CONS_EXPORTING_TEMPLATE_NAME],
        cons.CONS_CHANNEL: values[cons.CONS_CHANNEL],
        cons.CONS_TARGET_SAMPLE_RATE: values[cons.CONS_TARGET_SAMPLE_RATE],
        cons.CONS_DURATION: values[cons.CONS_DURATION],
        cons.CONS_CREATED_DATE: current_date, 
        cons.CONS_MODIFIED_DATE: current_date
    }
    output = exporting_template_col.insert_one(new_exporting_template_json)
    if output:
        print('exporting_template_id: ' + str(output))
    return output.inserted_id
