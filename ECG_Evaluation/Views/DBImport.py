import streamlit as st
import os
import tkinter as tk
from tkinter import filedialog
import numpy as np

def LoadForm():
    # Set up tkinter
    root = tk.Tk()
    root.withdraw()

    # Make folder picker dialog appear on top of other windows
    root.wm_attributes('-topmost', 1)

    # Folder picker button
    st.write('Please select a folder:')
    clicked = st.button('Folder Picker')
    if clicked:
        dirPath = filedialog.askdirectory(master=root)
        dirname = st.text_input('Selected folder:', dirPath)    
        # st.text(dirname) 
        filelist = []
        dirlist = []
        fileName=None
        for root, dirs, files in os.walk(dirname):
            for file in files:
                    filelist.append([file])
                    dirlist.append([dirPath + '/' + file])                   
                    if not fileName:
                        fileName = file.split(".")[0]
        st.text('File name: ' + dirname + '/' + fileName)
        # arr = np.concatenate((filelist, dirlist), axis=0) 
        # st.write(arr)
        #if not filelist or not dirlist:
        return np.concatenate((filelist, dirlist), axis=1) 