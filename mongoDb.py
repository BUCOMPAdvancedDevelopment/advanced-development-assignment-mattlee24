import pymongo 
from pymongo import MongoClient 
from bson.json_util import dumps
import requests
import json

cluster=MongoClient( "mongodb+srv://dpUser:dpUserPassword@adcoursework.9ybhyss.mongodb.net/?retryWrites=true&w=majority") 
db=cluster["Games"] 
collection=db["Games"] 

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

def edit_game(update_game, game_query):
    collection.update_one(game_query, update_game)
    return update_game

def add_game(new_game_json):
    collection.insert_one(new_game_json)
    return new_game_json


