import os
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, url_for, request, jsonify
import random

from utils.db import Db

load_dotenv()

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # One year in seconds

db = Db()

# Routes
@app.route('/')
def index():
    return redirect(url_for('dashboard'))

# Routes
@app.route('/login-subscriber', methods=['GET'])
def loginSubscriber():      
    station_id = request.args.get('station_id', 0)
    link_login_only = request.args.get('link_login_only', 'http://192.168.88.1')
    link_orig = request.args.get('link_orig', 'https://192.168.88.1')
    
    station = db.get_station(id=station_id)
    latest_videos = db.get_videos(station)
    #images uploaded at https://postimages.org/
    images = db.get_images(station)
    return render_template('login-subscriber.html', station=station, link_login_only=link_login_only, link_orig=link_orig,
                           video=random.sample(latest_videos, 1)[0], images=random.sample(images, 5))

@app.route('/add-subscriber', methods=['POST'])
def addSubscriber():    
    phone = request.form['phone']
    station_id = request.form['station_id']
    subscriber_id = db.add_subscriber(phone, station_id)
    return jsonify(
            {
                "subscriber_id": subscriber_id,
                "phone": phone,
                "station_id": station_id
            }
        )

@app.route('/terms', methods=['GET'])
def terms():        
    station_id = request.args.get('station_id', 0)
    station = db.get_station(id=station_id)
    return render_template('terms.html', station=station)

@app.route('/dashboard', methods=['GET'])
def dashboard(): 
    total_connections = db.get_total_connections()
    active_connections = db.get_total_connections(active=True)
    stations_connections = db.get_connection_counts_per_station()
    total_connections_today = db.get_total_connections(today=True)
    unique_connections_today = db.get_unique_connections(today=True)
    latest_connections = db.get_latest_connections()
    print(total_connections)
    return render_template('dashboard.html', 
                           total_connections=total_connections, active_connections=active_connections, 
                           stations_connections=stations_connections,
                           total_connections_today=total_connections_today,unique_connections_today=unique_connections_today,
                           latest_connections=latest_connections)

if __name__ == '__main__':
    debug_mode = os.getenv('IS_DEBUG', 'False') in ['True', 'T', 't', '1']
    app.run(debug=debug_mode)