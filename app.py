import logging, os
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, url_for, request 
from flask_cors import CORS

from utils import api, routes
from utils.database import init_db

load_dotenv()

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # One year in seconds
CORS(app)


# Global logging configuration (applies to all modules)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'  # Optional: Custom date format (e.g., 2025-11-04 22:13:45)
)
logger = logging.getLogger(__name__)


# Create tables at startup (sync, no async needed)
with app.app_context():
    init_db()
 
# API Routes
@app.route('/<hotspot_id>/api/portal-data', methods=['GET'])
def portalData(hotspot_id):
    return api.portal_data(hotspot_id)
 
@app.route('/<hotspot_id>/api/subscribe', methods=['POST'])
def subscribe(hotspot_id):
    return api.subscribe(hotspot_id)

# Web App Routes
@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard', methods=['GET'])
def dashboard(): 
    return routes.dashboard()

@app.route('/clients', methods=['GET', 'POST'])
def clients(): 
    return routes.clients()

@app.route('/hotspots', methods=['GET', 'POST'])
def hotspots(): 
    return routes.hotspots()

@app.route('/gallery', methods=['GET', 'POST'])
def gallery(): 
    return routes.gallery()

@app.route('/system-users', methods=['GET', 'POST'])
def system_users(): 
    return routes.system_users()

@app.route('/subscribers', methods=['GET', 'POST'])
def subscribers(): 
    return routes.subscribers()

if __name__ == '__main__':
    debug_mode = os.getenv('IS_DEBUG', 'False') in ['True', 'T', 't', '1']
    app.run(debug=debug_mode)