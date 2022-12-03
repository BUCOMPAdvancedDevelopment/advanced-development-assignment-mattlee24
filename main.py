import datetime
import os
import logging
from types import NoneType
import mongoDb
import json
import firebase_admin
import requests
from bson.json_util import dumps
from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from google.auth.transport import requests as grequests
from google.cloud import datastore
from firebase_admin import credentials, firestore, initialize_app
import google.oauth2.id_token


# Enable running on local dev environment
# Always comment lines 12 and 13 before running on the cloud, otherwise the app will NOT work
os.environ.setdefault("GCLOUD_PROJECT", "ad-gamezone")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (r"C:\Users\matth\Desktop\AdLocalCoursework\venv\application_default_credentials.json")

firebase_request_adapter = grequests.Request()

# [START gae_python38_datastore_store_and_fetch_user_times]
# [START gae_python3_datastore_store_and_fetch_user_times]
datastore_client = datastore.Client()

# [END gae_python3_datastore_store_and_fetch_user_times]
# [END gae_python38_datastore_store_and_fetch_user_times]
app = Flask(__name__)
app.config['SECRET_KEY'] = '929AE2F2113856B6'

# [START gae_python38_datastore_store_and_fetch_user_times]
# [START gae_python3_datastore_store_and_fetch_user_times]
def store_time(email, dt):
    entity = datastore.Entity(key=datastore_client.key('User', email, 'visit'))
    entity.update({
        'timestamp': dt
    })

    datastore_client.put(entity)


def fetch_times(email, limit):
    ancestor = datastore_client.key('User', email)
    query = datastore_client.query(kind='visit', ancestor=ancestor)
    query.order = ['-timestamp']

    times = query.fetch(limit=limit)

    return times

def add_user_details(gamertag, platform, genre, game, uid):
    entity = datastore.Entity(key=datastore_client.key('UserId', uid, 'userDetails'))
    entity.update({
        'timestamp': datetime.datetime.now(),
        'gamertag': gamertag,
        'platform': platform,
        'genre': genre,
        'FavouriteGame': game,
    })

    datastore_client.put(entity)

def fetch_user_details(uid, limit):
    ancestor = datastore_client.key('UserId', uid)
    query = datastore_client.query(kind='userDetails', ancestor=ancestor)
    query.order = ['-timestamp']

    query_results = list(query.fetch())

    if len(query_results) == 0:
        userData = "null"
    else:
        userData = query.fetch(limit=limit)


    return userData

"""
    delete_user_info() function deletes all the user's data from the google cloud datastore.
    :param user_id: The user's user id (set by firebaseAuth)
    :return: Returns a confirmation string
"""

def delete_user_details(user_id):

    ancestor = datastore_client.key('UserId', user_id)
    query = datastore_client.query(kind='userDetails', ancestor=ancestor)
    data = query.fetch()
    datastore_client.delete_multi(data)


@app.route('/')
@app.route('/index')
def root():
    # Verify Firebase auth.
    id_token = request.cookies.get("token")
    error_message = None
    claims = None
    times = None

    if id_token:
        try:
            # Verify the token against the Firebase Auth API
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)

            store_time(claims['email'], datetime.datetime.now())
            times = fetch_times(claims['email'], 10)

            print(times)

        except ValueError as exc:
            # This will be raised if the token is expired or any other
            # verification checks fail.
            error_message = str(exc)

    return render_template('index.html', user_data=claims, error_message=error_message, times=times)

@app.route('/home') 
def home(): 
    return render_template('home.html') 

@app.route('/about') 
def about(): 
    return render_template('about.html') 

@app.route('/games', methods=["GET", "POST"]) 
def games():

    if request.method == "POST":
        slug = request.form["gameSlug"]
        name = request.form["gameName"]
        release = request.form["gameReleaseDate"]
        rating = request.form["gameRating"]
        image = request.form["gameImage"]
        price = request.form["gamePrice"]
        description = request.form["gameDescription"]
 
        new_game_json = {
            "slug": slug,
            "name": name,
            "released": release,
            "rating": rating,
            "background_image": image,
            "price": price,
            "description": description,
        }
        new_game = json.dumps(new_game_json)
        mongoDb.add_game(new_game)

    cart = mongoDb.get_cart()
    data = mongoDb.get_games()
    return render_template('games.html', data=data, cart=cart) 

@app.route('/<slug>', methods=['GET'])
def single_game(slug):
    data=mongoDb.get_single_game(slug)
    id_token = request.cookies.get("token")
    claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)
    return render_template('gamesDetails.html', data=data, user_data=claims)

@app.route('/deleteGame/<slug>', methods=['DELETE'])
def delete_game(slug):
    mongoDb.delete_game(slug)
    return render_template('games.html')

@app.route('/basket') 
def storeBasket(): 
    cart = mongoDb.get_cart()
    return render_template("basket.html", cart=cart) 

@app.route('/addToCart/<name>/<userID>/<price>', methods=['POST'])
def addToCart(name, userID, price):
    mongoDb.add_game_to_cart(name, userID, price)
    return render_template('games.html')

@app.route('/deleteFromCart/<slug>', methods=['DELETE'])
def deleteFromCart(slug):
    print(slug)
    mongoDb.delete_game_from_cart(slug)
    return render_template('basket.html')

@app.route('/editgames', methods=["GET", "POST"]) 
def editgames():
    if request.method == "POST":
        slug = request.form["gameSlug"]
        name = request.form["gameName"]
        release = request.form["gameReleaseDate"]
        rating = request.form["gameRating"]
        image = request.form["gameImage"]
        price = request.form["gamePrice"]
        description = request.form["gameDescription"]

        update_game = {
            "$set": {
                "slug": slug,
                "name": name,
                "released": release,
                "rating": rating,
                "background_image": image,
                "price": price,
                "description": description,
            }
        }
        update_game = json.dumps(update_game)
        # print(json.loads(update_game))
        mongoDb.edit_game(update_game, slug)
    flash('Click on game to edit...', 'success')
    data = mongoDb.get_games()
    return render_template('edit_games.html', data=data) 

@app.route("/editgames/<slug>", methods=["GET", "POST"])
def editGame(slug):
    data=mongoDb.get_single_game(slug)
    return render_template("editGameDetails.html", data=data)

@app.route('/account', methods=["GET", "POST"]) 
def account(): 

    if request.method == "POST":
        user_id = request.form["user_id"]
    
        delete_user_details(user_id)

    id_token = request.cookies.get("token")

    claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)

    data = fetch_user_details(claims['user_id'], 1)

    return render_template('account.html', data=data, user_data=claims) 

@app.route('/accountInfo', methods=["GET", "POST"]) 
def accountInfo(): 

    id_token = request.cookies.get("token")

    claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)

    user_data = fetch_user_details(claims['user_id'], 1)

    if request.method == "POST":
        gamertag = request.form["gamertag"]
        platform = request.form["platform"]
        genre = request.form["genre"]
        game = request.form["game"]

        id_token = request.cookies.get("token")

        claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)
    
        add_user_details(gamertag, platform, genre, game, claims['user_id'])

        return redirect("/account")
        
    data = mongoDb.get_games()
    return render_template('accountInfo.html', data=data, user_data=user_data) 

# Only Used when running locally
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)