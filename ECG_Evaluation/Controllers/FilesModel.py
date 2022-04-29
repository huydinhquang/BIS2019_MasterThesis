class Files():
    def __init__(self,file_path=None,file_name_ext=None, file_name=None, output_data=None, ecg_id=None, channel=None, folder_download=None):
        self.file_path = file_path
        self.file_name_ext = file_name_ext
        self.file_name = file_name
        self.output_data = output_data
        self.ecg_id = ecg_id
        self.channel = channel
        self.folder_download = folder_download

    # getting the values
    @property
    def value(self):
        # print('Getting value')
        return self.file_path,self.file_name_ext,self.file_name, self.output_data, self.ecg_id, self.channel,self.folder_download
 
    # setting the values
    @value.setter
    def value(self,file_path,file_name_ext, file_name, output_data, ecg_id, channel,folder_download):
        # print('Setting value to: ' + source + ', File name: ' + file_name)
        self.file_path = file_path
        self.file_name_ext = file_name_ext
        self.file_name = file_name
        self.output_data = output_data
        self.ecg_id = ecg_id
        self.channel = channel
        self.folder_download = folder_download
        
    # deleting the values
    @value.deleter
    def value(self):
        # print('Deleting value')
        del self.file_path,self.file_name_ext,self.file_name, self.output_data, self.ecg_id, self.channel,self.folder_download