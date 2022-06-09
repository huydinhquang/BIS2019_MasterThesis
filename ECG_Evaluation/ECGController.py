from abc import ABC, abstractmethod
import Controllers.Common as common

class ECGController(ABC):
    def __init__(self, dir_name, file_name, file_list):
        self.dir_name = dir_name
        self.file_name = file_name
        self.file_list = file_list

    @property
    def full_name(self):
        return f"{self.dir_name} {self.file_name}"

    @property
    def current_date(self):
        return common.get_current_date()

    @abstractmethod
    def get_record_property(self):
        pass