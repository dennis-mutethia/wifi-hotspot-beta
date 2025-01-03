import os
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, url_for
import random

load_dotenv()

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # One year in seconds

# Routes
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET'])
def login():      
    link_login_only = "http://192.168.88.1"
    username = "GHDRSD"
    password = "FGSDVAT%^S"
    videos = ["vid_0.mp4","vid_1.mp4","vid_2.mp4"]
    images = ['img_0.jpg', 'img_1.jpg', 'img_2.jpg', 'img_3.jpg', 'img_4.jpg', 'img_5.jpg', 'img_6.jpg', 'img_7.jpg', 'img_8.jpg', 'img_9.jpg']
    return render_template('login.html', link_login_only=link_login_only, username=username, password=password,
                           video=random.sample(videos, 1)[0], images=random.sample(images, 5))

@app.route('/terms', methods=['GET'])
def terms():      
    return render_template('terms.html')

if __name__ == '__main__':
    debug_mode = os.getenv('IS_DEBUG', 'False') in ['True', '1', 't']
    app.run(debug=debug_mode)