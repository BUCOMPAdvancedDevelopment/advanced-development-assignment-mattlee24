import datetime
import os
import logging
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
        mongoDb.add_game(new_game_json)

    data = mongoDb.get_games()
    return render_template('games.html', data=data) 

@app.route('/<slug>', methods=['GET'])
def single_game(slug):
    data=mongoDb.get_single_game(slug)
    return render_template('gamesDetails.html', data=data)

@app.route('/deleteGame/<slug>', methods=['DELETE'])
def delete_game(slug):
    mongoDb.delete_game(slug)
    return render_template('games.html')

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

        game_query = {"slug": {"$eq": slug}}
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
        mongoDb.edit_game(update_game, game_query)
    flash('Click on game to edit...', 'success')
    data = mongoDb.get_games()
    return render_template('edit_games.html', data=data) 

@app.route("/editgames/<slug>", methods=["GET", "POST"])
def editGame(slug):
    jResponse=mongoDb.get_single_game(slug)
    data=json.loads(jResponse)
    return render_template("editGameDetails.html", data=data)

@app.route('/account') 
def account(): 
    return render_template('account.html') 

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.

    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='0.0.0.0', port=5000, debug=True)