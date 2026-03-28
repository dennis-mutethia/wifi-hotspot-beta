import hashlib, random
from flask import render_template, request, jsonify

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
   
def dashboard(db): 
    total_connections = db.get_total_connections()
    active_connections = db.get_total_connections(active=True)
    all_hotspots = db.get_hotspots(client_id=0)
    hotspots_connections = db.get_connection_counts_per_hotspot()
    total_connections_today = db.get_total_connections(today=True)
    unique_connections_today = db.get_unique_connections(today=True)
    connections_per_day = db.get_connections_per_day()
    connections_per_hour = db.get_connections_per_hour()
    latest_connections = db.get_latest_connections()
    return render_template('dashboard.html', page='dashboard',
                           total_connections=total_connections, active_connections=active_connections, 
                           all_hotspots=all_hotspots, hotspots_connections=hotspots_connections,
                           total_connections_today=total_connections_today,unique_connections_today=unique_connections_today,
                           connections_per_day=connections_per_day, latest_connections=latest_connections, connections_per_hour=connections_per_hour)
    
    
def clients(db): 
    if request.method == 'POST':   
        action = request.form['action'] 
        if action in ['add', 'edit']:
            client_name = request.form['clientName']
            client_phone = request.form['clientPhone']
            background_color = request.form['backgroundColor']
            foreground_color = request.form['foregroundColor']      
            if action == 'add':
                updated_client_id = db.update_client(None, client_name, client_phone, background_color, foreground_color)
                
            elif action == 'edit':
                edit_client_id = int(request.form['editClientId'])
                updated_client_id = db.update_client(edit_client_id, client_name, client_phone, background_color, foreground_color)
        
        elif action =='remove':
            remove_client_id = int(request.form['removeClientId'])
            db.remove_client(remove_client_id)
             
    clients = db.get_clients()
    return render_template('clients.html', page='clients', clients=clients)
    
    
def hotspots(db): 
    if request.method == 'POST':   
        action = request.form['action'] 
        if action in ['add', 'edit']:
            hotspot_name = request.form['hotspotName']
            client_id = request.form['clientId']      
            if action == 'add':
                added_hotspot_id = db.update_hotspot(None, hotspot_name, client_id)
                
            elif action == 'edit':
                edit_hotspot_id = int(request.form['editHotspotId'])
                updated_hotspot_id = db.update_hotspot(edit_hotspot_id, hotspot_name, client_id)
        
        elif action =='remove':
            remove_hotspot_id = int(request.form['removeHotspotId'])
            db.remove_hotspot(remove_hotspot_id)
      
    hotspots = db.get_hotspots()
    clients = db.get_clients() 
    return render_template('hotspots.html', page='hotspots', hotspots=hotspots, clients=clients)
    
    
def subscribers(db):       
    subscribers = db.get_subscribers()
    return render_template('subscribers.html', page='subscribers', subscribers=subscribers)


def gallery(db): 
    if request.method == 'POST':   
        action = request.form['action'] 
        if action in ['add', 'edit']:
            url = request.form['url']
            client_id = request.form['clientId']   
            hotspot_id = request.form['hotspotId']   
            
            if 'youtube' in url:
                type = 'video'
                source_id = url.replace('https://www.youtube.com/watch?v=', '')
            if 'postimg' in url:
                type = 'image'
                source_id = url.replace('https://i.postimg.cc/', '')
                   
            if action == 'add':
                added_media_id = db.update_media(None, type, source_id, client_id, hotspot_id)
                
            elif action == 'edit':
                edit_media_id = int(request.form['editMediaId'])
                updated_media_id = db.update_media(edit_media_id, type, source_id, client_id, hotspot_id)
        
        elif action =='remove':
            remove_media_id = int(request.form['removeMediaId'])
            db.remove_media(remove_media_id)
    
    
    hotspot_id = request.args.get('hotspotId', None)
    hotspot_id = int(hotspot_id) if hotspot_id else None
                
    media = db.get_media(hotspot_id=hotspot_id)
    images = [image for image in media if image.type == 'image']
    videos = [video for video in media if video.type == 'video']
    hotspots = db.get_hotspots()
    clients = db.get_clients() 
    return render_template('gallery.html', page='gallery', hotspots=hotspots, clients=clients, images=images, videos=videos, hotspot_id=hotspot_id)

    
def system_users(db): 
    if request.method == 'POST':   
        action = request.form['action'] 
        if action in ['add', 'edit']:
            name = request.form['systemUserName'].upper()
            phone = request.form['phone']
            client_id = request.form['clientId'] 
            if action == 'add':
                added_system_user_id = db.update_system_user(None, name, phone, client_id, password=hash_password(phone))
                
            elif action == 'edit':
                edit_system_user_id = int(request.form['editSystemUserId'])                
                updated_system_user_id = db.update_system_user(edit_system_user_id, name, phone, client_id)
        
        elif action =='remove':
            remove_system_user_id = int(request.form['removeSystemUserId'])
            db.remove_system_user(remove_system_user_id)

    system_users = db.get_system_users()
    clients = db.get_clients() 
    return render_template('system-users.html', page='system_users', system_users=system_users, clients=clients)