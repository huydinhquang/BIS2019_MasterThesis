import streamlit as st
import Views.DBImport as dbImport
import Controllers.MongoDBConnection as con
import Processor as processor
import Scraper as scraper

st.title('ECG System')

filelist = dbImport.LoadForm()
# if not filelist:
#     st.write('Cannot read source folder!')
#     st.stop()

st.text('File list:')
st.write(len(filelist))

for item in filelist:
    st.write(item)
    st.write(item[0])
    ecgProperty = processor.GetSourceProperty(item[0])
    # st.write(ecgProperty.source)
    # if not ecgProperty.source:
    #     st.write('Cannot read source property!')
    #     st.stop()

# myDB = con.connectMongoDB()
# myCol = con.connectMongoCollectionDB()

# fileID, ecgID = scraper.SaveECGData(myDB, myCol, r"C:\Users\HuyDQ\OneDrive\HuyDQ\OneDrive\MasterThesis\Thesis\DB\MIT\100.dat", "100.dat", ecgProperty)

# if fileID:
#     if ecgID:
#         st.write('Imported successfully!')
#     else:
#         st.write('Import failed with ECG Property!')
# else:
#     st.write('Import failed with Database source!')
