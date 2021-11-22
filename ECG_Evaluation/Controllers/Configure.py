import Controllers.SecretKeys as sk

class Configure():
    def get_configure_value(self):
        value = sk.format_descriptor
        format_desciptor = value.split(";")
        return format_desciptor