from ECGController import ECGController

class SciPyController(ECGController):
    def __init__(self, dir_name, file_name, test1, test2):
        super().__init__(dir_name, file_name)
        self.test1 = test1
        self.test2 = test2

    def get_source_property(self):
        return self.test1 * self.test2