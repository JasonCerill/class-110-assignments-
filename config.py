
import pymongo
import certifi


con_str = "mongodb+srv://jasoncerfsdi:newpassword@cluster0.hqmhe.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(con_str, tlsCAFile=certifi.where())

db = client.get_database("FoodStore")