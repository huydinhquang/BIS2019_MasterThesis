from ECGController import ECGController
import streamlit as st
from Controllers.ECGModel import ECG
import wfdb
import pandas as pd
import Controllers.Constants as cons
import Controllers.Common as common
import os
from pathlib import Path
import shutil
import numpy as np
import matplotlib.pyplot as plt
import Views.DBImport as db_import
import Views.AnnotationExtractor as ann_extract

class WFDBController(ECGController):
    def __init__(self, dir_name, file_name):
        super().__init__(dir_name, file_name)

    def get_source_property(self):
        try:
            signals, fields = wfdb.rdsamp(self.dir_name + '/' + self.file_name)
            # headers = wfdb.rdheader(dir_name + '/' + file_name)
            fs = fields[cons.SAMPLING_FREQUENCY]
            time = round(len(signals) / fs)
            channels = [item.upper() for item in fields[cons.SINGAL_NAME]] 
            return ECG(
                id=None,
                source=None,
                file_name=self.file_name,
                channel=channels,
                record=len(signals),
                time=time,
                sample_rate=fs,
                ecg=None,
                created_date=self.current_date,
                modified_date=self.current_date
            )
        except ValueError:
            e = RuntimeError('Cannot read source property!')
            st.exception(e)
