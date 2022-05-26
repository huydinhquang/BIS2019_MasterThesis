from ECGController import ECGController
import scipy.io
from Controllers.ECGModel import ECG
import Controllers.Constants as cons

class SciPyController(ECGController):
    def __init__(self, dir_name, file_name, file_list):
        super().__init__(dir_name, file_name, file_list)

    def get_source_property(self):
        mat = scipy.io.loadmat(self.file_list[0])
        signals = mat[cons.CONS_ECG]
        return ECG(
            file_name=self.file_name,
            sample=signals,
            ecg=len(self.file_list), # Total number of ECG files
            created_date=self.current_date,
            modified_date=self.current_date
        )
