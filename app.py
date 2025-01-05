import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
import random

from utils.db import Db

load_dotenv()

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # One year in seconds

db = Db()

station = "Club Country - Muthiga Inn"

# Routes
@app.route('/', methods=['GET'])
def index():      
    client_id = request.args.get('cid', 0)
    station_id = request.args.get('sid', 0)
    link_login_only = "http://192.168.88.1"
    username = "GHDRSD"
    password = "FGSDVAT%^S"
    latest_videos = db.get_videos(liveBroadcastContent='none', limit=4)
    #images uploaded at https://postimg.cc/
    images = ['Ff3WDnqT/img-0.jpg', '63kFnCSH/img-1.jpg', '15ZLzcDX/img-2.jpg', '7hSdVfrq/img-3.jpg', 'gchCdBX1/img-4.jpg', 'K8GwPGqy/img-5.jpg', '9FtswRBp/img-6.jpg', 'VN5hh7PG/img-7.jpg', '1zTd1p99/img-8.jpg', 'YCdV85ZL/img-9.jpg']
    return render_template('login.html', station=station, link_login_only=link_login_only, 
                           username=username, password=password,
                           video=random.sample(latest_videos, 1)[0], images=random.sample(images, 5))

@app.route('/terms', methods=['GET'])
def terms():      
    return render_template('terms.html', station=station)

if __name__ == '__main__':
    debug_mode = os.getenv('IS_DEBUG', 'False') in ['True', 'T', 't', '1']
    app.run(debug=debug_mode)