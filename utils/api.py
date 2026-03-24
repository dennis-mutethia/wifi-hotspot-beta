import random, re
from flask import request, jsonify

def to_dict(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

def portal_data(db, hotspot_id): 
    if request.method == 'GET':               
        hotspot = db.get_hotspots(id=int(hotspot_id))[0]
        client = db.get_clients(id=hotspot.client_id)[0]
        media = db.get_media(client_id=client.id, hotspot_id=hotspot.id)
        
        images = [image for image in media if image.type == 'image']
        videos = [video for video in media if video.type == 'video']
        
        return jsonify({
            "client": client.to_dict(),
            "hotspot": hotspot.to_dict(),
            "video": [v.to_dict() for v in random.sample(videos, min(1, len(images)))][0] if videos else None,
            "images": [i.to_dict() for i in random.sample(images, min(5, len(images)))]
        })
        
def subscribe(db): 
    if request.method == 'POST':   
        phone = request.form['phone']
        hotspot_id = int(request.form['hotspot_id'])
        hotspot = db.get_hotspots(id=hotspot_id)[0]
        
        # Get device info
        user_agent = request.headers.get('User-Agent')
        match = re.search(r'\(([^)]+)\)', user_agent)
        device = match.group(1) if match else None
        
        subscriber_id = db.add_subscriber(phone, hotspot_id, hotspot.client_id, device=device)

        return jsonify({
            "username": subscriber_id % 251,
            "password": "TgdV84"
        })