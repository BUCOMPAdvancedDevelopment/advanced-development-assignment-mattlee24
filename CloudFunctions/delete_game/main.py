import pymongo
from pymongo import MongoClient
from bson.json_util import dumps
import os
import requests
import json
# end imports

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