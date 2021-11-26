import Controllers.SecretKeys as sk
import Controllers.Constants as cons

class Configure():
    def get_configure_value(self):
        format_desciptor = get_format_descriptor()
        channel_name = get_channel_name()
        result = {
            cons.FORMAT_DESCRIPTOR: format_desciptor,
            cons.CHANNEL_NAME: channel_name
        }
        return result
    
def get_format_descriptor():
    value = sk.format_descriptor
    return value.split(";")

def get_channel_name():
    value = sk.channel_name
    return value.split(";")