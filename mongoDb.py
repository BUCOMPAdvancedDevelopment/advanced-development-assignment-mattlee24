import pymongo 
from pymongo import MongoClient 
from bson.json_util import dumps

cluster=MongoClient( "mongodb+srv://dpUser:dpUserPassword@adcoursework.9ybhyss.mongodb.net/?retryWrites=true&w=majority") 
db=cluster["Games"] 
collection=db["Games"] 

def get_mongodb_items():
    # Search data from Mongodb

    myCursor = None
    # create queries
    name_query = {"name": {"$eq": "Grand Theft Auto V"}}

    myCursor = collection.find()
    list_cur = list(myCursor)
    json_data = dumps(list_cur)
    return json_data

def get_single_game(slug):
    # Search data from Mongodb

    myCursor = None
    # create queries
    game_query = {"slug": {"$eq": slug}}
    name_query = {"name": {"$eq": "Grand Theft Auto V"}}

    myCursor = collection.find({"$and": [game_query]})
    list_cur = list(myCursor)
    json_data = dumps(list_cur)
    return json_data