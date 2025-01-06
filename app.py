import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
import random

from utils.db import Db

load_dotenv()

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # One year in seconds

db = Db()

# Routes
@app.route('/login-subscriber', methods=['GET'])
def index():      
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
    return render_template('terms.html', station=station,)

if __name__ == '__main__':
    debug_mode = os.getenv('IS_DEBUG', 'False') in ['True', 'T', 't', '1']
    app.run(debug=debug_mode)