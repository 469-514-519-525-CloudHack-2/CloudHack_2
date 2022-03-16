from matplotlib import collections
from pymongo import MongoClient

host=MongoClient("172.17.0.2")  #docker inspect 
# host=MongoClient("mongodb")

db=host["consumerDB"]

collection=db["consumers"]

sample_data={
    "name":"hello",
    "hobby":"nothing"
}


collection.insert_one(sample_data)
print('Inserted into the MongoDB database!')

rec_data = collection.find_one({"name":"hello"})
print("Fecthed from MongoDB: ",rec_data)
