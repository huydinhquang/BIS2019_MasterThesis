import streamlit as st
import json
from bson import json_util

def parse_json(data):
    return json.loads(json_util.dumps(data, indent = 4, sort_keys = True, default = str))

def render_text_success(text):
    st.markdown(f'<p style="color:green;">{text}</p>', unsafe_allow_html=True)