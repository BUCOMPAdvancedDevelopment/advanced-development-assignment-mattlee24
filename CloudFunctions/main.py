import pymongo
from pymongo import MongoClient
from bson.json_util import dumps
import os
import requests
import json
# end imports

def get_mongodb_items(request):
    # Search data from Mongodb
    cluster=MongoClient( "mongodb+srv://dpUser:dpUserPassword@adcoursework.9ybhyss.mongodb.net/?retryWrites=true&w=majority") 
    db=cluster["Games"] 
    collection=db["Games"] 

    myCursor = None

    myCursor = collection.find()
    list_cur = list(myCursor)
    json_data = dumps(list_cur)
    return json_data

def get_single_game(request):
    # Search data from Mongodb 
    cluster=MongoClient( "mongodb+srv://dpUser:dpUserPassword@adcoursework.9ybhyss.mongodb.net/?retryWrites=true&w=majority") 
    db=cluster["Games"] 
    collection=db["Games"] 

    passed_slug = request.args.get('slug')

    myCursor = None
    # create queries
    game_query = {"slug": {"$eq": passed_slug}}

    myCursor = collection.find({"$and": [game_query]})
    list_cur = list(myCursor)
    json_data = dumps(list_cur)
    return json_data

def delete_game(request):
    # Search data from Mongodb
    cluster=MongoClient( "mongodb+srv://dpUser:dpUserPassword@adcoursework.9ybhyss.mongodb.net/?retryWrites=true&w=majority") 
    db=cluster["Games"] 
    collection=db["Games"] 

    passed_slug = request.args.get('slug')

    myCursor = None
    # create queries
    game_query = {"slug": {"$eq": passed_slug}}
    collection.delete_one({"$and": [game_query]})
    
    return passed_slug


def edit_game(request):
    # Search data from Mongodb 
    cluster=MongoClient( "mongodb+srv://dpUser:dpUserPassword@adcoursework.9ybhyss.mongodb.net/?retryWrites=true&w=majority") 
    db=cluster["Games"] 
    collection=db["Games"] 

    passed_slug = request.args.get('slug')
    passed_update_game = request.args.get('update_game')

    game_query = {"slug": {"$eq": passed_slug}}
    update_game = json.loads(passed_update_game)
    
    collection.update_one(game_query, update_game)
    return update_game

def add_game(request):
    # Search data from Mongodb 
    cluster=MongoClient( "mongodb+srv://dpUser:dpUserPassword@adcoursework.9ybhyss.mongodb.net/?retryWrites=true&w=majority") 
    db=cluster["Games"] 
    collection=db["Games"] 

    passed_new_game = json.loads(request.args.get('new_game'))
    
    collection.insert_one(passed_new_game)
    return new_game