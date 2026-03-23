import random
from flask import render_template, request, jsonify

def portal_data(db): 
    if request.method == 'GET':       
        hotspot_id = int(request.args.get('hotspot_id', 0))
        
        hotspot = db.get_hotspots(id=hotspot_id)[0]
        client = db.get_clients(id=hotspot.client_id)[0]
        media = db.get_media(client_id=client.id, hotspot_id=hotspot.id) or db.get_videos(client_id=client.id) 
        images = [image for image in media if image.type == 'image']
        videos = [video for video in media if video.type == 'video']
         

        return jsonify(
                {
                    "client": client,
                    "hotspot": hotspot,
                    "video": random.sample(videos, min(1, len(videos)))[0] if videos else None,
                    "images": random.sample(images, min(5, len(images)))
                }
            ) 
        
def subscribe(db): 
    if request.method == 'POST':   
        phone = request.form['phone']
        hotspot_id = int(request.form['hotspot_id'])
        hotspot = db.get_hotspots(id=hotspot_id)[0]
        subscriber_id = db.add_subscriber(phone, hotspot_id, hotspot.client_id)  

        return jsonify(
                {
                    "subscriber_id": subscriber_id,
                    "phone": phone,
                    "hotspot_id": hotspot_id
                }
            ) 