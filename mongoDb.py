import requests
import json
from pymongo import MongoClient
from bson.json_util import dumps

def get_games():
    url = "https://europe-west2-ad-gamezone.cloudfunctions.net/get_mongodb_games"

    uResponse = requests.get(url)
    jResponse = uResponse.text
    data = json.loads(jResponse)

    return data

def get_single_game(slug):
    url = ("https://europe-west2-ad-gamezone.cloudfunctions.net/get_single_game?slug=" + slug)

    uResponse = requests.get(url)
    jResponse = uResponse.text
    data = json.loads(jResponse)

    return data

def delete_game(slug):
    url = ("https://europe-west2-ad-gamezone.cloudfunctions.net/delete_game?slug=" + slug)
    uResponse = requests.get(url)
    uResponse
    return "game deleted"

def edit_game(update_game, slug):
    url = ("https://europe-west2-ad-gamezone.cloudfunctions.net/edit_game?slug=" + slug + "&update_game=" + update_game)
    uResponse = requests.get(url)
    uResponse
    return update_game

def add_game(new_game):
    url = ("https://europe-west2-ad-gamezone.cloudfunctions.net/add_game?new_game=" + new_game)
    uResponse = requests.get(url)
    uResponse
    return new_game

def add_game_to_cart(name, userID, price):
    cluster=MongoClient( "mongodb+srv://dpUser:dpUserPassword@adcoursework.9ybhyss.mongodb.net/?retryWrites=true&w=majority") 
    db=cluster["Games"] 
    collection=db["Cart"] 
    new_item = {
        "userID": userID,
        "name": name,
        "price": price,
    }
    collection.insert_one(new_item)
    return new_item

def delete_game_from_cart(slug):
    cluster=MongoClient( "mongodb+srv://dpUser:dpUserPassword@adcoursework.9ybhyss.mongodb.net/?retryWrites=true&w=majority") 
    db=cluster["Games"] 
    collection=db["Cart"] 

    item_query = {"name": {"$eq": slug}}
    print(item_query)
    collection.delete_one({"$and": [item_query]})

    return slug

def get_cart():
    cluster=MongoClient( "mongodb+srv://dpUser:dpUserPassword@adcoursework.9ybhyss.mongodb.net/?retryWrites=true&w=majority") 
    db=cluster["Games"] 
    collection=db["Cart"] 

    list_cur = list(collection.find())
    json_data = dumps(list_cur)
    data = json.loads(json_data)

    return data


