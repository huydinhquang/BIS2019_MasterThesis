class ECG:
    @classmethod
    def __init__(self, source, fileName, channel, record, time, sampleRate, ecg):
        self.Source = source
        self.FileName = fileName
        self.Channel = channel
        self.Record = record
        self.Time = time
        self.SampleRate = sampleRate
        self.ECG = ecg

    # getting the values
    @property
    def value(self):
        print('Getting value')
        return self.Source, self.FileName, self.Channel, self.Record, self.Time, self.SampleRate, self.ECG
 
    # setting the values
    @value.setter
    def value(self, source, fileName, channel, record, time, sampleRate, ecg):
        print('Setting value to ' + source)
        self.Source = source
        self.FileName = fileName
        self.Channel = channel
        self.Record = record
        self.Time = time
        self.SampleRate = sampleRate
        self.ECG = ecg
 
    # deleting the values
    @value.deleter
    def value(self):
        print('Deleting value')
        del self.Source, self.Source, self.FileName, self.Channel, self.Record, self.Time, self.SampleRate, self.ECG