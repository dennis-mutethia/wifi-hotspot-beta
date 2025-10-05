import random
from flask import render_template, request, jsonify

def subscriber(db): 
    if request.method == 'GET':       
        hotspot_id = int(request.args.get('hotspot_id', 0))
        link_login_only = request.args.get('link_login_only', 'http://192.168.88.1')
        
        hotspot = db.get_hotspots(id=hotspot_id)[0]
        client = db.get_clients(id=hotspot.client_id)[0]
        media = db.get_media(client_id=client.id, hotspot_id=hotspot.id) or db.get_videos(client_id=client.id) #Youtube videos or images uploaded at https://postimages.org/
        images = [image for image in media if image.type == 'image']
        videos = [video for video in media if video.type == 'video']
        return render_template('login-subscriber.html', hotspot=hotspot, client=client, link_login_only=link_login_only,
                            video=random.sample(videos, min(1, len(videos)))[0], 
                            images=random.sample(images, min(5, len(images))))
        
    elif request.method == 'POST':   
        phone = request.form['phone']
        hotspot_id = int(request.args.get('hotspot_id', 0))
        hotspot = db.get_hotspots(id=hotspot_id)[0]
        subscriber_id = db.add_subscriber(phone, hotspot_id, hotspot.client_id)  

        return jsonify(
                {
                    "subscriber_id": subscriber_id,
                    "phone": phone,
                    "hotspot_id": hotspot_id
                }
            ) 
    
def dashboard(db): 
    total_connections = db.get_total_connections()
    active_connections = db.get_total_connections(active=True)
    all_hotspots = db.get_hotspots(client_id=0)
    hotspots_connections = db.get_connection_counts_per_hotspot()
    total_connections_today = db.get_total_connections(today=True)
    unique_connections_today = db.get_unique_connections(today=True)
    connections_per_day = db.get_connections_per_day()
    latest_connections = db.get_latest_connections()
    return render_template('dashboard.html', page='dashboard',
                           total_connections=total_connections, active_connections=active_connections, 
                           all_hotspots=all_hotspots, hotspots_connections=hotspots_connections,
                           total_connections_today=total_connections_today,unique_connections_today=unique_connections_today,
                           connections_per_day=connections_per_day, latest_connections=latest_connections)
    
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
            hotspot_username = request.form['hotspotUsername']
            hotspot_password = request.form['hotspotPassword']
            client_id = request.form['clientId']      
            if action == 'add':
                added_hotspot_id = db.update_hotspot(None, hotspot_name, hotspot_username, hotspot_password, client_id)
                
            elif action == 'edit':
                edit_hotspot_id = int(request.form['editHotspotId'])
                updated_hotspot_id = db.update_hotspot(edit_hotspot_id, hotspot_name, hotspot_username, hotspot_password, client_id)
        
        elif action =='remove':
            remove_hotspot_id = int(request.form['removeHotspotId'])
            db.remove_hotspot(remove_hotspot_id)
      
    hotspots = db.get_hotspots()
    clients = db.get_clients() 
    return render_template('hotspots.html', page='hotspots', hotspots=hotspots, clients=clients)


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
            
    media = db.get_media() #Youtube videos or images uploaded at https://postimages.org/
    images = [image for image in media if image.type == 'image']
    videos = [video for video in media if video.type == 'video']
    hotspots = db.get_hotspots()
    clients = db.get_clients() 
    return render_template('gallery.html', page='gallery', hotspots=hotspots, clients=clients, images=images, videos=videos)