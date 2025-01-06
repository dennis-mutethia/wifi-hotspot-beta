import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
import random

from utils.db import Db

load_dotenv()

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # One year in seconds

db = Db()
station = {
    'id': 1,
    'name' : 'Club X Lounge',
    'hotspotUsername' : 'GHDRSD',
    'hotspotPassword' : 'FGSDVAT%^S',
    'createdAt': None,
    'client' : {
        'id': 20,
        'name' : 'Club X Lounge',
        'backgroundColor': 'red',
        'foregroundColor': 'white',
        'createdAt': None
    }
}    

# Routes
@app.route('/', methods=['GET'])
def index():      
    station_id = request.args.get('station_id', 0)
    link_login_only = request.args.get('link_login_only', 'http://192.168.88.1')
    link_orig = request.args.get('link_orig', 'http://192.168.88.1')
    
    #station = db.get_station(station_id)
    latest_videos = db.get_videos(liveBroadcastContent='none', limit=4)
    latest_videos = [
        {
            'id': 1,
            'videoId' : 'qdWniWOZqIE',
            'publishedAt' : None,
            'clientId' : 20,
            'stationId' : 3
        }
    ]
    #images uploaded at https://postimages.org/
    images = ['Ff3WDnqT/img-0.jpg', '63kFnCSH/img-1.jpg', '15ZLzcDX/img-2.jpg', '7hSdVfrq/img-3.jpg', 'gchCdBX1/img-4.jpg', 'K8GwPGqy/img-5.jpg', '9FtswRBp/img-6.jpg', 'VN5hh7PG/img-7.jpg', '1zTd1p99/img-8.jpg', 'YCdV85ZL/img-9.jpg']
    return render_template('index.html', station=station, link_login_only=link_login_only, link_orig=link_orig,
                           video=random.sample(latest_videos, 1)[0], images=random.sample(images, 5))

@app.route('/terms', methods=['GET'])
def terms():        
    station_id = request.args.get('station_id', 0)
    #station = db.get_station(station_id)
    return render_template('terms.html', station=station,)

if __name__ == '__main__':
    debug_mode = os.getenv('IS_DEBUG', 'False') in ['True', 'T', 't', '1']
    app.run(debug=debug_mode)