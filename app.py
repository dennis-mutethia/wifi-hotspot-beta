import os
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, url_for, request 

#neon login = 
from utils.db import Db
from utils import routes

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
    return routes.subscriber(db)

@app.route('/add-subscriber', methods=['POST'])
def addSubscriber():     
    return routes.subscriber(db)

@app.route('/terms', methods=['GET'])
def terms():        
    hotspot_id = request.args.get('hotspot_id', 0)
    hotspot = db.get_hotspot(id=hotspot_id)
    return render_template('terms.html', hotspot=hotspot)

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

if __name__ == '__main__':
    debug_mode = os.getenv('IS_DEBUG', 'False') in ['True', 'T', 't', '1']
    app.run(debug=debug_mode)