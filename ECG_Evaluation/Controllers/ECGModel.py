class ECG():
    def __init__(self, source, file_name, channel, record, time, sample_rate, ecg, created_date, modified_date):
        self.source = source
        self.file_name = file_name
        self.channel = channel
        self.record = record
        self.time = time
        self.sample_rate = sample_rate
        self.ecg = ecg
        self.created_date = created_date
        self.modified_date = modified_date

    # getting the values
    @property
    def value(self):
        # print('Getting value')
        return self.source, self.file_name, self.channel, self.record, self.time, self.sample_rate, self.ecg, self.created_date, self.modified_date
 
    # setting the values
    @value.setter
    def value(self, source, file_name, channel, record, time, sample_rate, ecg, created_date, modified_date):
        # print('Setting value to: ' + source + ', File name: ' + file_name)
        self.source = source
        self.file_name = file_name
        self.channel = channel
        self.record = record
        self.time = time
        self.sample_rate = sample_rate
        self.ecg = ecg
        self.created_date = created_date
        self.modified_date = modified_date
 
    # deleting the values
    @value.deleter
    def value(self):
        # print('Deleting value')
        del self.source, self.file_name, self.channel, self.record, self.time, self.sample_rate, self.ecg, self.created_date, self.modified_date