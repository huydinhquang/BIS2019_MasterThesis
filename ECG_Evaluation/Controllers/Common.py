import streamlit as st
import json
from bson import json_util
import bson.objectid
import datetime

def parse_json(data):
    return json.loads(json_util.dumps(data, indent = 4, sort_keys = True, default = str))

def render_text_success(text):
    st.markdown(f'<p style="color:green;">{text}</p>', unsafe_allow_html=True)

def render_text_error(text):
    st.markdown(f'<p style="color:red;">{text}</p>', unsafe_allow_html=True)

def my_handler(x):
    # st.write(x)
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    elif isinstance(x, bson.objectid.ObjectId):
        return str(x)
    else:
        raise TypeError(x)