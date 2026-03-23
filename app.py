import os
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, url_for, request 

#neon login = 
from utils.db import Db
from utils import api, routes

load_dotenv()

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # One year in seconds

db = Db()

# API Routes
@app.route('/api/portal-data', methods=['GET'])
def portalData():
    return api.portal_data(db)

@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    return api.subscribe(db)


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

@app.route('/subscribers', methods=['GET', 'POST'])
def subscribers(): 
    return routes.subscribers(db)

if __name__ == '__main__':
    debug_mode = os.getenv('IS_DEBUG', 'False') in ['True', 'T', 't', '1']
    app.run(debug=debug_mode)