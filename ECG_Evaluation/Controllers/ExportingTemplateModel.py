class ExportingTemplate():
    def __init__(self, exporting_template_name=None, channel=None, target_sample_rate=None, duration=None, created_date=None, modified_date=None, id=None):
        self.exporting_template_name = exporting_template_name
        self.channel = channel
        self.target_sample_rate = target_sample_rate
        self.duration = duration
        self.created_date = created_date
        self.modified_date = modified_date
        self.id = id
        
        
    # getting the values
    @property
    def value(self):
        # print('Getting value')
        return self.exp_tem_name, self.channel, self.target_sample_rate, self.duration, self.created_date, self.modified_date, self.id
 
    # setting the values
    @value.setter
    def value(self, exporting_template_name, channel, target_sample_rate, duration, created_date, modified_date, id):
        self.exporting_template_name = exporting_template_name
        self.target_sample_rate = target_sample_rate
        self.duration = duration
        self.created_date = created_date
        self.modified_date = modified_date
        self.id = id
        self.channel = channel
        
    # deleting the values
    @value.deleter
    def value(self):
        # print('Deleting value')
        del self.exporting_template_name, self.channel, self.target_sample_rate, self.duration, self.created_date, self.modified_date, self.id