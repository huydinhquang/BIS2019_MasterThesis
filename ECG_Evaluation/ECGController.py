from abc import ABC, abstractmethod
from datetime import datetime

class ECGController(ABC):
    def __init__(self, dir_name, file_name):
        self.dir_name = dir_name
        self.file_name = file_name

    @property
    def full_name(self):
        return f"{self.dir_name} {self.file_name}"

    @property
    def current_date(self):
        return datetime.now()

    @abstractmethod
    def get_source_property(self):
        pass

    # @abstractmethod
    # def get_source_property_constraint(self):
    #     pass

    # @abstractmethod
    # def render_property(self):
    #     pass
