import os
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, url_for, request 
from flask_cors import CORS

#neon login = 
from utils.db import Db
from utils import api, routes

load_dotenv()

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # One year in seconds
CORS(app)

db = Db()

# API Routes
@app.route('/api/portal-data/<hotspot_id>', methods=['GET'])
def portalData(hotspot_id):
    return api.portal_data(db, hotspot_id)

@app.route('/api/subscribe/<hotspot_id>', methods=['POST'])
def subscribe(hotspot_id):
    return api.subscribe(db, hotspot_id)

# Web App Routes
@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/add-subscriber', methods=['POST'])
def addSubscriber():     
    return routes.subscriber(db)

@app.route('/terms', methods=['GET'])
def terms():        
    hotspot_id = int(request.args.get('hotspot_id', 0))
    hotspot = db.get_hotspots(id=hotspot_id)[0]
    client = db.get_clients(id=hotspot.client_id)[0]
    return render_template('terms.html', hotspot=hotspot, client=client)

@app.route('/dashboard', methods=['GET'])
def dashboard(): 
    return routes.dashboard(db)

@app.route('/clients', methods=['GET', 'POST'])
def clients(): 
    return routes.clients(db)

@app.route('/hotspots', methods=['GET', 'POST'])
def hotspots(): 
    return routes.hotspots(db)

@app.route('/gallery', methods=['GET', 'POST'])
def gallery(): 
    return routes.gallery(db)

@app.route('/system-users', methods=['GET', 'POST'])
def system_users(): 
    return routes.system_users(db)

@app.route('/subscribers', methods=['GET', 'POST'])
def subscribers(): 
    return routes.subscribers(db)

if __name__ == '__main__':
    debug_mode = os.getenv('IS_DEBUG', 'False') in ['True', 'T', 't', '1']
    app.run(debug=debug_mode)