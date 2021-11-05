import streamlit as st
import Controllers.Constants as cons

mongo = st.secrets[cons.MONGOCONNECTIONSTR]
db_name = st.secrets[cons.MONGODB][cons.DBNAME]
collection_name = st.secrets[cons.MONGODB][cons.COLLECTIONNAME]
