import Controllers.Common as common
import Controllers.Constants as cons
from ECG_Evaluation.Controllers.ExportingTemplateModel import ExportingTemplate

def add_exporting_template(exporting_template_col, values:ExportingTemplate):
    exp_tem_name = values.exporting_template_name
    list_channel = values.channel
    target_sample_rate = values.target_sample_rate
    duration = values.duration

    current_date = common.get_current_date()
    new_exporting_template_json = {
        cons.CONS_EXPORTING_TEMPLATE_NAME: exp_tem_name,
        cons.CONS_CHANNEL: list_channel,
        cons.CONS_TARGET_SAMPLE_RATE: target_sample_rate,
        cons.CONS_DURATION: duration,
        cons.CONS_CREATED_DATE: current_date, 
        cons.CONS_MODIFIED_DATE: current_date
    }
    output = exporting_template_col.insert_one(new_exporting_template_json)
    if output:
        print('exporting_template_id: ' + str(output))
    return output.inserted_id
