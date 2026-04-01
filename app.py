import logging, os
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, url_for, request 
from flask_cors import CORS

from utils.routes.api import API
from utils.routes.dashboard import DashboardRoute
from utils.routes.clients import ClientsRoute
from utils.routes.gallery import GalleryRoute
from utils.routes.hotspots import HotspotsRoute
from utils.routes.subscribers import SubscribersRoute
from utils.routes.system_users import SystemUsersRoute
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
    return API().portal_data(hotspot_id)
 
@app.route('/<hotspot_id>/api/subscribe', methods=['POST'])
def subscribe(hotspot_id):
    return API().subscribe(hotspot_id)


# Web App Routes
@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard', methods=['GET'])
def dashboard(): 
    return DashboardRoute()()

@app.route('/clients', methods=['GET', 'POST'])
def clients(): 
    return ClientsRoute()()

@app.route('/hotspots', methods=['GET', 'POST'])
def hotspots(): 
    return HotspotsRoute()()

@app.route('/gallery', methods=['GET', 'POST'])
def gallery(): 
    return GalleryRoute()()

@app.route('/system-users', methods=['GET', 'POST'])
def system_users(): 
    return SystemUsersRoute()()

@app.route('/subscribers', methods=['GET', 'POST'])
def subscribers(): 
    return SubscribersRoute()()

if __name__ == '__main__':
    debug_mode = os.getenv('IS_DEBUG', 'False') in ['True', 'T', 't', '1']
    app.run(debug=debug_mode)