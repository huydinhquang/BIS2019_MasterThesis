class Files():
    def __init__(self, file_name, output_data, ecg_id, channel):
        self.file_name = file_name
        self.output_data = output_data
        self.ecg_id = ecg_id
        self.channel = channel

    # getting the values
    @property
    def value(self):
        # print('Getting value')
        return self.file_name, self.output_data, self.ecg_id, self.channel
 
    # setting the values
    @value.setter
    def value(self, file_name, output_data, ecg_id, channel):
        # print('Setting value to: ' + source + ', File name: ' + file_name)
        self.file_name = file_name
        self.output_data = output_data
        self.ecg_id = ecg_id
        self.channel = channel
        
    # deleting the values
    @value.deleter
    def value(self):
        # print('Deleting value')
        del self.file_name, self.output_data, self.ecg_id, self.channel