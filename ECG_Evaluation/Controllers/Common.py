import pytz
import streamlit as st
import json
from bson import json_util
from datetime import datetime, timedelta
from dateutil import tz
import Controllers.Constants as cons

def parse_json(data):
    return json.loads(json_util.dumps(data, indent = 4, sort_keys = True, default = str))

def render_text_success(text):
    st.markdown(f'<p style="color:green;">{text}</p>', unsafe_allow_html=True)

def render_text_error(text):
    st.markdown(f'<p style="color:red;">{text}</p>', unsafe_allow_html=True)

def convert_list_to_string(list):
    return '; '.join(str(item) for item in list)

def convert_timestamp_to_datetime(value):
    time_stamp_value = value[cons.CONS_DATE_STR]
    timestamp = datetime.fromtimestamp(time_stamp_value/1000.0)
    timestamp_formatted = timestamp.strftime("%d.%m.%Y %H:%M:%S")
    return timestamp_formatted

def convert_time_to_datetime(value):
    # Get local timezone
    local_zone = tz.tzlocal()
    
    # Convert timezone of datetime from UTC to local
    dt_local = value.astimezone(local_zone)
    dt_offset = dt_local.tzinfo._std_offset.seconds
    new_timestamp = timedelta(seconds=dt_offset)
    local_time = value + new_timestamp
    
    # Format the local datetime
    local_time_str = local_time.strftime("%d.%m.%Y %H:%M:%S")
    return local_time_str

def convert_current_time_to_str():
    datetime_str = get_current_date().strftime("%Y%m%d_%H%M%S")
    return datetime_str

def convert_string_to_list(string, separator, hasSpacebar = False):
    if (hasSpacebar):
        return list(string.split(f'{separator} '))
    else:    
        return list(string.split(f'{separator}'))

def get_current_date():
    return datetime.now(tz=pytz.UTC)

# def my_handler(x):
#     # st.write(x)
#     if isinstance(x, datetime.datetime):
#         return x.isoformat()
#     elif isinstance(x, bson.objectid.ObjectId):
#         return str(x)
#     else:
#         raise TypeError(x)