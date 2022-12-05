import pymongo
from pymongo import MongoClient
from bson.json_util import dumps
import os
import requests
import json
# end imports

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