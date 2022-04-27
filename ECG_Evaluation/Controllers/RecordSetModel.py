class RecordSet():
    def __init__(self, record_set_name=None, source=None, created_date=None, modified_date=None, id=None):
        self.record_set_name = record_set_name
        self.created_date = created_date
        self.modified_date = modified_date
        self.id = id
        self.source = source
        
    # getting the values
    @property
    def value(self):
        # print('Getting value')
        return self.record_set_name, self.created_date, self.modified_date, self.id, self.source
 
    # setting the values
    @value.setter
    def value(self, record_set_name, source, created_date, modified_date, id):
        self.record_set_name = record_set_name
        self.created_date = created_date
        self.modified_date = modified_date
        self.id = id
        self.source = source
        
    # deleting the values
    @value.deleter
    def value(self):
        # print('Deleting value')
        del self.record_set_name, self.created_date, self.modified_date, self.id, self.source