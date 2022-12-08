import requests
import json
from pymongo import MongoClient
from bson.json_util import dumps

"""
    the following functions, up to the next comment, call the functions from the cloud and returns the correct data and/or
    passes in the correct variables the cloud functions needs
"""

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

"""
    The following functions access mongoDB with values passed from main.py. These funcions allow the pages
    basket and myOrders to run correctly and remain persistent
"""

def get_cartbyID(userID, total):
    cluster=MongoClient( "mongodb+srv://dpUser:dpUserPassword@adcoursework.9ybhyss.mongodb.net/?retryWrites=true&w=majority") 
    db=cluster["Games"] 
    collection=db["Cart"] 
    collectionOrders=db["Orders"] 

    myCursor = None

    orderTotal = total

    orderItems = []

    item_query = {"userID": {"$eq": userID}}

    myCursor = collection.find({"$and": [item_query]})

    for item in myCursor:
        orderItems.append(str(item['name']))
        collection.delete_one(item)
    new_item = {
        "userID": userID,
        "gameNames": orderItems,
        "cost": orderTotal,
    }

    collectionOrders.insert_one(new_item)

    return userID

def add_game_to_cart(name, userID, price, image):
    cluster=MongoClient( "mongodb+srv://dpUser:dpUserPassword@adcoursework.9ybhyss.mongodb.net/?retryWrites=true&w=majority") 
    db=cluster["Games"] 
    collection=db["Cart"] 
    new_item = {
        "userID": userID,
        "name": name,
        "price": price,
        "image": image,
    }
    collection.insert_one(new_item)
    return new_item

def delete_game_from_cart(name):
    cluster=MongoClient( "mongodb+srv://dpUser:dpUserPassword@adcoursework.9ybhyss.mongodb.net/?retryWrites=true&w=majority") 
    db=cluster["Games"] 
    collection=db["Cart"] 

    item_query = {"name": {"$eq": name}}
    print(item_query)
    collection.delete_one({"$and": [item_query]})

    return name

def get_cart():
    cluster=MongoClient( "mongodb+srv://dpUser:dpUserPassword@adcoursework.9ybhyss.mongodb.net/?retryWrites=true&w=majority") 
    db=cluster["Games"] 
    collection=db["Cart"] 

    list_cur = list(collection.find())
    json_data = dumps(list_cur)
    data = json.loads(json_data)

    return data

def get_orders(userID):
    cluster=MongoClient( "mongodb+srv://dpUser:dpUserPassword@adcoursework.9ybhyss.mongodb.net/?retryWrites=true&w=majority") 
    db=cluster["Games"] 
    collection=db["Orders"] 

    item_query = {"userID": {"$eq": userID}}

    list_cur = list(collection.find({"$and": [item_query]}))
    json_data = dumps(list_cur)
    data = json.loads(json_data)

    return data


