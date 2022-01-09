from ECGController import ECGController
import scipy.io
from Controllers.ECGModel import ECG

class SciPyController(ECGController):
    def __init__(self, dir_name, file_name, file_list):
        super().__init__(dir_name, file_name, file_list)

    def get_source_property(self):
        mat = scipy.io.loadmat(self.file_list[0][1])
        signals = mat['ecg']
        return ECG(
            file_name=self.file_name,
            sample=signals,
            created_date=self.current_date,
            modified_date=self.current_date
        )