class ExportingRegion():
    def __init__(self, record_set_id=None, ecg_id=None, start_time=None, end_time=None, sample_from=None, sample_to=None, created_date=None, modified_date=None, id=None, is_update=None):
        self.record_set_id = record_set_id
        self.ecg_id = ecg_id
        self.start_time = start_time
        self.end_time = end_time
        self.sample_from = sample_from
        self.sample_to = sample_to
        self.modified_date = modified_date
        
        if not is_update:
            self.created_date = created_date
            self.id = id

    # getting the values
    @property
    def value(self):
        # print('Getting value')
        return self.record_set_id, self.ecg_id, self.start_time, self.end_time, self.sample_from, self.sample_to, self.created_date, self.modified_date, self.id
 
    # setting the values
    @value.setter
    def value(self, record_set_id, ecg_id, start_time, end_time, sample_from, sample_to, created_date, modified_date, id):
        self.record_set_id = record_set_id
        self.ecg_id = ecg_id
        self.start_time = start_time
        self.end_time = end_time
        self.sample_from = sample_from
        self.sample_to = sample_to
        self.created_date = created_date
        self.modified_date = modified_date
        self.id = id
        
    # deleting the values
    @value.deleter
    def value(self):
        # print('Deleting value')
        del self.record_set_id, self.ecg_id, self.start_time, self.end_time, self.sample_from, self.sample_to, self.created_date, self.modified_date, self.id