
import pymongo
from pymongo import MongoClient
from bson.json_util import dumps
import os
import requests
import json
# end imports

def add_game(request):
    # Search data from Mongodb 
    cluster=MongoClient( "mongodb+srv://dpUser:dpUserPassword@adcoursework.9ybhyss.mongodb.net/?retryWrites=true&w=majority") 
    db=cluster["Games"] 
    collection=db["Games"] 

    passed_new_game = json.loads(request.args.get('new_game'))
    
    collection.insert_one(passed_new_game)
    return passed_new_game