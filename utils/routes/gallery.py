
import logging
from flask import render_template, request, jsonify
from sqlmodel import select, func
from uuid import UUID

from utils.database import get_session
from utils.models import Clients, Hotspots, Media

logger = logging.getLogger(__name__)
    

class GalleryRoute:
    def __init__(self):
        pass

    def __call__(self):          
        session = get_session()
        try:
            if request.method == 'POST':
                action = request.form['action']
                if action in ['add', 'edit']:
                    link = request.form['source'] #https://www.youtube.com/watch?v=MaZLKAx6Ne0                
                    client_id = UUID(request.form['clientId'])
                    hotspot_id = UUID(request.form['hotspotId'])

                    if 'youtube' in link:
                        media_type = 'video'
                        video_id_match = re.search(r'(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})', link)
                        source = f"https://www.youtube.com/embed/{video_id_match.group(1)}"
                    elif 'postimg' in link:
                        media_type = 'image'
                        source = link
                    else:
                        return jsonify({"error": "Unsupported URL"}), 400

                    if action == 'add':
                        media = Media(type=media_type, source=source, client_id=client_id, hotspot_id=hotspot_id)
                        session.add(media)

                    elif action == 'edit':
                        media_id = UUID(request.form['editMediaId'])
                        media = session.execute(
                            select(Media).where(Media.id == media_id)
                        ).scalar_one()
                        media.type = media_type
                        media.source_id = source_id
                        media.client_id = client_id
                        media.hotspot_id = hotspot_id

                elif action == 'remove':
                    media_id = UUID(request.form['removeMediaId'])
                    media = session.execute(
                        select(Media).where(Media.id == media_id)
                    ).scalar_one()
                    session.delete(media)

                session.commit()

        except Exception as e:
            logger.error(f"Error in saving gallery: {e}")
            images, videos, hotspots, clients = [], [], [], []
            hotspot_id = None
        
        finally:
            try:
                client_id = request.args.get('clientId', None)
                hotspot_id = request.args.get('hotspotId', None)
                hotspot_id = UUID(hotspot_id) if hotspot_id else None
                
                media_query = select(Media)
                if client_id:
                    media_query = media_query.where(Media.client_id == client_id)
                if hotspot_id:
                    media_query = media_query.where(Media.hotspot_id == hotspot_id)

                media = session.execute(media_query).scalars().all()
                images = [m for m in media if m.type == 'image']
                videos = [m for m in media if m.type == 'video']
                hotspots = session.execute(select(Hotspots).order_by(Hotspots.name)).scalars().all()
                clients = session.execute(select(Clients).order_by(Clients.name)).scalars().all()
                
            except Exception as e:
                logger.error(f"Error closing session in gallery: {e}")
                images, videos, hotspots, clients = [], [], [], []
                hotspot_id = None
        
        return render_template('gallery.html', page='gallery', hotspots=hotspots, clients=clients,
                            images=images, videos=videos, client_id=client_id, hotspot_id=hotspot_id)

