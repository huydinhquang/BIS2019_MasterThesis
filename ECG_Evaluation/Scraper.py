import streamlit as st
import gridfs
import Controllers.ECGModel as ecgModel
import Controllers.Common as common

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
    ecgProperty.ecg = [fileID]
    # jsonECGPropertyStr = json.dumps(ecgProperty.__dict__)
    jsonECGPropertyStr = common.parse_json(ecgProperty.__dict__)
    output = myCol.insert_one(jsonECGPropertyStr)
    return output

def SaveECGData(myDB, myCol, filePath, fileName, ecgProperty: ecgModel.ECG):
    file = ImportDB(myDB, filePath, fileName)
    fileID = file._id
    st.write(fileID)
    if fileID:
        ecg = SaveECGProperty(myCol, ecgProperty, fileID)
        ecgID = ecg.inserted_id
        st.write(ecgID)
        if ecgID:
            return fileID, ecgID
        else:
            # TODO: Delete source file if the ECG Property can't be inserted
            return fileID, None
    else:
        return None, None