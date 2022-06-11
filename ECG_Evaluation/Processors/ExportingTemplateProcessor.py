from bson.objectid import ObjectId
from pymongo import helpers
import streamlit as st
from Controllers.ECGModel import ECG
import wfdb
from datetime import datetime
import pandas as pd
import Controllers.Constants as cons
import Controllers.Common as common
import Scraper as scraper
import Scrapers.RecordSetScraper as record_set_scraper

class ExportingTemplateProcessor:
    st.write('test')