import streamlit as st
import Views.DBImport as dbImport
import Controllers.MongoDBConnection as con
import Processor as processor
import Scraper as scraper
import os
import tkinter as tk
from tkinter import filedialog
import numpy as np

st.title('ECG System')
importDB = None


def ProcessFile(dirName):
    fileList = []
    dirlist = []
    fileName = None
    for root, dirs, files in os.walk(dirName):
        for file in files:
            fileList.append([file])
            dirlist.append([dirPath + '/' + file])
            if not fileName:
                fileName = file.split(".")[0]
    if not fileList or not dirlist:
        st.write('Cannot read source folder!')
        st.stop()
    return np.concatenate((fileList, dirlist), axis=1), fileName


def ImportDB():
    listFileID = []
    for item in fileList:
        ecgProperty = processor.GetSourceProperty(fileName, dirName)
        st.write(ecgProperty.source)
        if not ecgProperty.source:
            st.write('Cannot read source property!')
            st.stop()

        # Open MongoDB connection
        myDB = con.connectMongoDB()
        myCol = con.connectMongoCollectionDB()

        # Save ECG file to MongoDB
        fileID = scraper.SaveECGFile(
            myDB, myCol, item[1], item[0], ecgProperty)
        if fileID:
            listFileID.append([fileID])
    ecgID = scraper.SaveECGProperty(myCol, ecgProperty, listFileID)
    if ecgID:
        print('ECGId: ' + str(ecgID))
        st.write('Imported successfully!')


def ReadProperty(fileName, dirName):
    ecgProperty = processor.GetSourceProperty(fileName, dirName)
    # st.write(ecgProperty.channel)
    if not ecgProperty.channel:
        st.write('Cannot read source property!')
        st.stop()

    col1, col2, col3 = st.columns(3)
    with col1:
        title = st.text_input('Source name', 'Test')
        st.text('Total records')
        totalRecords = st.text(str(ecgProperty.record))
    with col2:
        options = st.multiselect(
            'Channel(s)',
            ['I', 'II', 'III',
             'aVR', 'aVL', 'aVF',
             'V1', 'V2', 'V3',
             'V4', 'V5', 'V6'])
        st.text('Total channels')
        st.text(str(len(options)))
    with col3:
        sampleRate = st.slider('Sample rate', 0, 10000,
                               ecgProperty.sample_rate)
        st.text('Time(s)')
        times = st.text(str(ecgProperty.time))

    importDB = st.button('Import source')

# Set up tkinter
root = tk.Tk()
root.withdraw()

# Make folder picker dialog appear on top of other windows
root.wm_attributes('-topmost', 1)

# Folder picker button
st.text('Please select a folder:')
clicked = st.button('Folder Picker')
if clicked:
    dirPath = filedialog.askdirectory(master=root)
    dirName = st.text_input('Selected folder:', dirPath)
    # Process to get the list of files when selecting the folder
    fileList, fileName = ProcessFile(dirName)

    # Read ECG properties when user selects a source
    ReadProperty(fileName, dirName)
