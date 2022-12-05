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