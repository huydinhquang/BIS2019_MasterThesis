import streamlit as st
import pymongo

# Initialize connection.
client = pymongo.MongoClient(**st.secrets["mongo"])

# Pull data from the collection.
# Uses st.cache to only rerun when the query changes or after 10 min.
# @st.cache(ttl=600)
def get_data():
    # db = client.mydb
    mydb = client["ECG"]
    mycol = mydb["ECGTest"]
    # st.write(mycol)
    return mycol
    # mycol.update_many({}, {"$set": {"country1": "country2"}})
    # items = db.mycollection.find()
    # items = list(items)  # make hashable for st.cache
    # return items

items = get_data()

mylist = [
  { "name": "Amy", "address": "Apple st 652"},
  { "name": "Viola", "address": "Sideway 1633"}
]

x = items.insert_many(mylist)

#print list of the _id values of the inserted documents:
print(x.inserted_ids)

# st.sidebar.selectbox ("Select collection: ", items.list_collection_names())

# st.write(items)
# items.update_many({}, {"$set": {"country1": "country2"}})

# Print results.
# for item in items:
#     st.write(f"{item['Source']} has a :{item['FileName']}:")
#     st.write(item)