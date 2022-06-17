import Controllers.SecretKeys as sk
import Controllers.Constants as cons

class Configure():
    def get_configure_value(self):
        format_desciptor = get_format_descriptor()
        channel_name = get_channel_name()

        result = {
            cons.CONF_FORMAT_DESCRIPTOR: format_desciptor,
            cons.CONF_CHANNEL_NAME: channel_name,
            cons.CONF_FOLDER_IMPORT_RECORD: sk.default_folder_import_record,
            cons.CONF_FOLDER_IMPORT_RECORD_MASS: sk.default_folder_import_record_mass,
            cons.CONF_FOLDER_EXPORT_DATA: sk.default_folder_export_data,
            cons.CONF_FOLDER_TEMP: sk.default_folder_temp
        }
        return result
    
def get_format_descriptor():
    value = sk.format_descriptor
    return value.split(";")

def get_channel_name():
    value = sk.channel_name
    return value.split(";")