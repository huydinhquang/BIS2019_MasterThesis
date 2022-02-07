import streamlit as st
import json
from bson import json_util
import bson.objectid
import datetime as dt
import Controllers.Constants as cons

def parse_json(data):
    return json.loads(json_util.dumps(data, indent = 4, sort_keys = True, default = str))

def render_text_success(text):
    st.markdown(f'<p style="color:green;">{text}</p>', unsafe_allow_html=True)

def render_text_error(text):
    st.markdown(f'<p style="color:red;">{text}</p>', unsafe_allow_html=True)

def convert_list_to_string(list):
    return ', '.join(str(item) for item in list)

def convert_timestamp_to_datetime(value):
    time_stamp_value = value[cons.CONS_DATE_STR]
    timestamp = dt.datetime.fromtimestamp(time_stamp_value/1000.0)
    timestamp_formatted = timestamp.strftime("%d.%m.%Y %H:%M:%S")
    return timestamp_formatted

def convert_time_to_datetime(value):
    timestamp_formatted = value.strftime("%d.%m.%Y %H:%M:%S")
    return timestamp_formatted

def convert_string_to_list(string):
    return list(string.split(', '))

# def my_handler(x):
#     # st.write(x)
#     if isinstance(x, datetime.datetime):
#         return x.isoformat()
#     elif isinstance(x, bson.objectid.ObjectId):
#         return str(x)
#     else:
#         raise TypeError(x)