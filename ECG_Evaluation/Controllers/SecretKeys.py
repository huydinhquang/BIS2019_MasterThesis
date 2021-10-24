import streamlit as st
import Controllers.Constants as cons

mongo = st.secrets[cons.MongoConnectionStr]
dbName = st.secrets[cons.MongoDB][cons.DBName]
collectionName = st.secrets[cons.MongoDB][cons.CollectionName]
