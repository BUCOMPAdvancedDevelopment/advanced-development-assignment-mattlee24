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

def delete_game(slug):
    game_query = {"slug": {"$eq": slug}}
    collection.delete_one({"$and": [game_query]})
    return slug

def edit_game(update_game, game_query):
    collection.update_one(game_query, update_game)
    return update_game

def add_game(new_game_json):
    collection.insert_one(new_game_json)
    return new_game_json


