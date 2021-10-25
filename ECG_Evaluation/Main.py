import streamlit as st
# import Views.Components as mc
import Controllers.MongoDBConnection as con
import Processor as processor
import Scraper as scraper

st.title('This is a Huy test website')
# mc.Print()

ecgProperty = processor.GetSourceProperty(r"C:\Users\HuyDQ\OneDrive\HuyDQ\OneDrive\MasterThesis\Thesis\DB\MIT\100.dat")
st.write(ecgProperty.source)
if not ecgProperty.source:
    st.write('Cannot read source property!')
    st.stop()

myDB = con.connectMongoDB()
myCol = con.connectMongoCollectionDB()

fileID, ecgID = scraper.SaveECGData(myDB, myCol, r"C:\Users\HuyDQ\OneDrive\HuyDQ\OneDrive\MasterThesis\Thesis\DB\MIT\100.dat", "100.dat", ecgProperty)

if fileID:
    if ecgID:
        st.write('Imported successfully!')
    else:
        st.write('Import failed with ECG Property!')
else:
    st.write('Import failed with Database source!')
