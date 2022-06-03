from abc import ABC, abstractmethod
from datetime import datetime

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
        return datetime.now()

    @abstractmethod
    def get_record_property(self):
        pass