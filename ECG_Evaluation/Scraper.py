import streamlit as st
import gridfs
import json
import Controllers.ECGModel as ecgModel

def ImportDB(myDB, filePath, fileName):
    try:
        fileData = open(filePath, "rb")
        data = fileData.read()
        fs = gridfs.GridFS(myDB)
        result = fs.put(data, filename = fileName)
        output = fs.get(result)
        return output
    except ValueError:
        st.write('Please check your file path!')
        st.stop()

def SaveECGProperty(myCol, ecgProperty: ecgModel.ECG, fileID):
    # ecgData = { "Source": "MIT", "FileName" : "100", "Channel": 2, "Record": 11520000, "Time": 1800, "Sample rate": 500, "ECG" : ['', id]}
    st.write(fileID)
    ecgProperty.ECG = fileID
    st.write(ecgProperty.ECG)
    # jsonECGPropertyStr = json.dumps(ecgProperty.__dict__)
    jsonECGPropertyStr = json.dumps(ecgProperty, default=lambda x: x.__dict__)
    output = myCol.insert_one(jsonECGPropertyStr)
    return output

def SaveECGData(myDB, myCol, filePath, fileName, ecgProperty: ecgModel.ECG):
    file = ImportDB(myDB, filePath, fileName)
    fileID = file._id
    st.write(fileID)
    if fileID:
        st.write('Vao day hok? 1')
        ecg = SaveECGProperty(myCol, ecgProperty, fileID)
        ecgID = ecg.inserted_id
        st.write(ecgID)
        if ecgID:
            st.write('Vao day hok? 2')
            return fileID, ecgID
        else:
            return fileID, None
    else:
        return None, None