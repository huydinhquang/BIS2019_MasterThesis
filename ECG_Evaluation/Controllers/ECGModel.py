class ECG():
    def __init__(self, source, file_name, channel, record, time, sample_rate, ecg):
        self.source = source
        self.file_name = file_name
        self.channel = channel
        self.record = record
        self.time = time
        self.sample_rate = sample_rate
        self.ecg = ecg

    # getting the values
    @property
    def value(self):
        print('Getting value')
        return self.source, self.file_name, self.channel, self.record, self.time, self.sample_rate, self.ecg
 
    # setting the values
    @value.setter
    def value(self, source, file_name, channel, record, time, sample_rate, ecg):
        print('Setting value to ' + source)
        self.source = source
        self.file_name = file_name
        self.channel = channel
        self.record = record
        self.time = time
        self.sample_rate = sample_rate
        self.ecg = ecg
 
    # deleting the values
    @value.deleter
    def value(self):
        print('Deleting value')
        del self.source, self.file_name, self.channel, self.record, self.time, self.sample_rate, self.ecg