import requests
import json

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


