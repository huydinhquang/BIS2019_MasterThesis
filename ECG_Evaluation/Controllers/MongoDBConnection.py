import streamlit as st
import pymongo as pym
import Controllers.SecretKeys as sk

# Initialize connection.
client = pym.MongoClient(**sk.mongo)

# # Write down mongo data
# st.write(st.secrets[cons.MongoConnectionStr])
# st.write(st.secrets[cons.MongoDB])

# Retrieve DB and Collection names


# # Write down mongoDB data
# st.write(dbName)
# st.write(collectionName)

# Pull data from the collection.
# Uses st.cache to only rerun when the query changes or after 10 min.
# @st.cache(hash_funcs={pym.MongoClient: id, })
def connectMongoDB():
    return client[sk.dbName]

def connectMongoCollectionDB():
    db = connectMongoDB()
    return db[sk.collectionName]
    
#items = connectMongoDB()
# st.write('Count: '+ str(len(items)))

# Print results.
# for item in items:
#     st.write(f"{item['Source']} has a :{item['FileName']}:")
