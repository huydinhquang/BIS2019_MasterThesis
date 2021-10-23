import streamlit as st
import os
import wfdb
import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
from pymongo import MongoClient
import gridfs

st.title('This is a Huy test website')

import streamlit as st
import pandas as pd

# Load some example data.
DATA_URL = \
    "http://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz"
data = st.cache(pd.read_csv)(DATA_URL, nrows=1000)

# Select some rows using st.multiselect. This will break down when you have >1000 rows.
st.write('### Full Dataset', data)
selected_indices = st.multiselect('Select rows:', data.index)
selected_rows = data.loc[selected_indices]
st.write('### Selected Rows', selected_rows)

uploaded_files = st.file_uploader("Upload Files", accept_multiple_files=True,type=['dat','hea'])
for uploaded_file in uploaded_files:
    st.write("filename:", uploaded_file.name)
    bytes_data = uploaded_file.read()
    st.text(bytes_data)
#     uploaded_file.

# Set up tkinter
root = tk.Tk()
root.withdraw()

# Make folder picker dialog appear on top of other windows
root.wm_attributes('-topmost', 1)

def my_function():
    test = st.sidebar.selectbox(
        "Record(s)",
        ("Email", "Home phone", "Mobile phone")
        )
    st.write(test)

def signalProcess(dirname):
    signals, fields = wfdb.rdsamp(dirname + '/' + fileName)
    fs = fields['fs']
    time = round(len(signals) / fs)
    chanels = len(signals[0])
    st.text('Channel(s): ' + str(chanels))   
    st.text('Record(s): ' + str(len(signals)))
    st.text('Time(s): ' + str(time))
    st.text('Sample rate: ' + str(fs))
#     visualizeChart(signals, fs, chanels)


def visualizeChart(signals, fs, channels):
    for channel in range(channels):        
        #     wfdb.plot_items(signal=signals, fs=fields['fs'], title='Huy Test')
        #     st.pyplot(signals)
        signals, fields = wfdb.rdsamp(dirname + '/' + fileName, channels=[channel])
        timeArray = np.arange(signals.size) / fs
        plt.plot(timeArray, signals)
        plt.xlabel("time in s")
        plt.ylabel("ECG in mV")
        st.pyplot(plt)
        
# Folder picker button
st.write('Please select a folder:')
clicked = st.button('Folder Picker')
if clicked:
    dirname = st.text_input('Selected folder:', filedialog.askdirectory(master=root))    
    #st.text(dirname) 
    filelist=[]
    fileName=None
    for root, dirs, files in os.walk(dirname):
          for file in files:
                filelist.append(file)
                with open(dirname + '/' + file) as input:
                    st.text(input.read())
                if not fileName:
                    fileName = file.split(".")[0]
    st.text('File name: ' + dirname + '/' + fileName)
    st.write(filelist)
#     signals, fields = wfdb.rdsamp(dirname + '/' + fileName, channels=[0])
#     signalProcess(dirname)
#     my_function()


resultImport = st.button('Import')
if resultImport:
    client = MongoClient('mongodb+srv://admin:vi9mXNjbmf62mDjE@cluster0.ni6go.mongodb.net/myFirstDatabase?authSource=admin&replicaSet=atlas-u6guud-shard-0&w=majority&readPreference=primary&appname=MongoDB%20Compass&retryWrites=true&ssl=true')
    mydb = client["ECG"]
    mycol = mydb["ECGTest"]
    
    file_location = r"C:\Users\HuyDQ\OneDrive\HuyDQ\OneDrive\MasterThesis\Thesis\DB\MIT\100.dat"
    file_data = open(file_location, "rb")
    data = file_data.read()
    fs = gridfs.GridFS(mydb)
    result = fs.put(data, filename = '100.dat')
    st.write('Import completed')
    
    outdata = fs.get(result)
    outdata._id
    
    ecgData = { "Source": "MIT", "FileName" : "100", "Channel": 2, "Record": 11520000, "Time": 1800, "Sample rate": 500, "ECG" : ['4f0c76e46794dc6453000001', outdata._id]}
    x = mycol.insert_one(ecgData)
    st.write(x.inserted_id)
    
#     mylist = [
#       { "name": "Amy", "address": "Apple st 652"},
#       { "name": "Hannah", "address": "Mountain 21"},
#       { "name": "Michael", "address": "Valley 345"},
#       { "name": "Sandy", "address": "Ocean blvd 2"},
#       { "name": "Betty", "address": "Green Grass 1"},
#       { "name": "Richard", "address": "Sky st 331"},
#       { "name": "Susan", "address": "One way 98"},
#       { "name": "Vicky", "address": "Yellow Garden 2"},
#       { "name": "Ben", "address": "Park Lane 38"},
#       { "name": "William", "address": "Central st 954"},
#       { "name": "Chuck", "address": "Main Road 989"},
#       { "name": "Viola", "address": "Sideway 1633"}
#     ]

#     x = mycol.insert_many(mylist)

    #print list of the _id values of the inserted documents:
#     print(x.inserted_ids)
    
    
# result = client['sample_restaurants']['restaurants'].find(
#   filter=filter
# )

# for doc in result:
#     st.write(doc)

# client = pymongo.MongoClient("mongodb+srv://admin:vi9mXNjbmf62mDjE@cluster0.ni6go.mongodb.net/sample_restaurants")

# def query(country,keywords):

#     result = client['sample_restaurants']['restaurants'].aggregate([
#         {
#             '$search': {
#                 'text': {
#                     'path': [
#                         'industry'
#                     ], 
#                     'query': [
#                         ' %s' % (keywords)
#                     ], 
#                     'fuzzy': {
#                         'maxEdits': 2, 
#                         'prefixLength': 2
#                     }
#                 }
#             }
#         }, {
#             '$project': {
#                 'Name': '$name', 
#                 'URL': '$domain', 
#                 'Industry': '$industry', 
#                 'University': '$Uni', 
#                 'City': '$locality', 
#                 'Country': '$country', 
#                 'score': {
#                     '$meta': 'searchScore'
#                 }
#             }
#         }, {
#             '$match': {
#                 'Country': '%s' % (country)
#             }
#         }, {
#             '$limit': 10
#         }
#     ])

#     df = pd.DataFrame(result)

#     return df

# if st.button('Search'):
# #     df = query(country,phrases)
#     st.write(result)

# if test == 'Email':
#     city_options = {
#         5: "Arizona - Chandler - 5",
#         4: "Arizona - Phoenix - 4",
#         3: "New Jersey - Newark -3",
#         2: "Oregon - Portland - 2",
#         1: "Seattle - Washington - 1",
#     }

#     city_mode = st.sidebar.radio(
#         label="Choose a city option:",
#         options= (5, 4, 3, 2, 1),
#         format_func=lambda x: city_options.get(x),
#     )
#     st.write(city_mode)
# else:
#     st.write('not email')
#     st.write('aaa')
#     st.button('test 123')

# display = ("male", "female")

# options = list(range(len(display)))

# value = st.selectbox("gender", options, format_func=lambda x: display[x])

# st.write(value)

