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
    hotspot_id = request.args.get('hotspot_id', 0)
    link_login_only = request.args.get('link_login_only', 'http://192.168.88.1')
    link_orig = request.args.get('link_orig', 'https://192.168.88.1')
    
    hotspot = db.get_hotspot(id=hotspot_id)
    latest_videos = db.get_videos(hotspot)
    #images uploaded at https://postimages.org/
    images = db.get_images(hotspot)
    return render_template('login-subscriber.html', hotspot=hotspot, link_login_only=link_login_only, link_orig=link_orig,
                           video=random.sample(latest_videos, 1)[0], images=random.sample(images, 5))

@app.route('/add-subscriber', methods=['POST'])
def addSubscriber():    
    phone = request.form['phone']
    hotspot_id = request.form['hotspot_id']
    hotspot = db.get_hotspot(id=hotspot_id)
    subscriber_id = db.add_hotspot_user(phone, hotspot_id, hotspot.client.id)
    return jsonify(
            {
                "subscriber_id": subscriber_id,
                "phone": phone,
                "hotspot_id": hotspot_id
            }
        )

@app.route('/terms', methods=['GET'])
def terms():        
    hotspot_id = request.args.get('hotspot_id', 0)
    hotspot = db.get_hotspot(id=hotspot_id)
    return render_template('terms.html', hotspot=hotspot)

@app.route('/dashboard', methods=['GET'])
def dashboard(): 
    total_connections = db.get_total_connections()
    active_connections = db.get_total_connections(active=True)
    all_hotspots = db.get_all_hotspots(client_id=0)
    hotspots_connections = db.get_connection_counts_per_hotspot()
    total_connections_today = db.get_total_connections(today=True)
    unique_connections_today = db.get_unique_connections(today=True)
    connections_per_day = db.get_connections_per_day()
    latest_connections = db.get_latest_connections()
    return render_template('dashboard.html', page='dashboard',
                           total_connections=total_connections, active_connections=active_connections, 
                           all_hotspots=all_hotspots, hotspots_connections=hotspots_connections,
                           total_connections_today=total_connections_today,unique_connections_today=unique_connections_today,
                           connections_per_day=connections_per_day, latest_connections=latest_connections)

@app.route('/clients', methods=['GET'])
def clients(): 
    clients = db.get_all_clients()
    return render_template('clients.html', page='clients',
                           clients=clients)

if __name__ == '__main__':
    debug_mode = os.getenv('IS_DEBUG', 'False') in ['True', 'T', 't', '1']
    app.run(debug=debug_mode)