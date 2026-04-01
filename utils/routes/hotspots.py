
import logging
from flask import render_template, request, jsonify
from sqlmodel import select, func
from uuid import UUID

from utils.database import get_session
from utils.models import Clients, Hotspots, Subscribers

logger = logging.getLogger(__name__)
    

class HotspotsRoute:
    def __init__(self):
        pass

    def __call__(self):        
        session = get_session()
        try:
            if request.method == 'POST':
                action = request.form['action']
                if action in ['add', 'edit']:
                    name = request.form['hotspotName']
                    client_id = UUID(request.form['clientId'])

                    if action == 'add':
                        hotspot = Hotspots(name=name, client_id=client_id)
                        session.add(hotspot)

                    elif action == 'edit':
                        hotspot_id = UUID(request.form['editHotspotId'])
                        hotspot = session.execute(
                            select(Hotspots).where(Hotspots.id == hotspot_id)
                        ).scalar_one()
                        hotspot.name = name
                        hotspot.client_id = client_id

                elif action == 'remove':
                    hotspot_id = UUID(request.form['removeHotspotId'])
                    hotspot = session.execute(
                        select(Hotspots).where(Hotspots.id == hotspot_id)
                    ).scalar_one()
                    session.delete(hotspot)

                session.commit()

        except Exception as e:
            logger.error(f"Error saving hotspot: {e}")
            hotspots, clients = [], []
        
        finally:
            try:
                clients = session.execute(select(Clients).order_by(Clients.name)).scalars().all()
                
                rows = session.execute(
                    select(
                        Hotspots, 
                        func.count(Subscribers.id).label("subscribers")
                    )
                    .join(Subscribers, Hotspots.id == Subscribers.hotspot_id, isouter=True)
                    .group_by(Hotspots.id)
                    .order_by(Hotspots.name)
                ).all()
                
                hotspots = [
                    {
                        "id": h.id,
                        "name": h.name,
                        "client_id": h.client_id,
                        "subscribers": count or 0,
                    }
                    for h, count in rows
                ]
            
                session.close()
                
            except Exception as e:
                logger.error(f"Error closing session in system_users: {e}")
        
        
        return render_template('hotspots.html', page='hotspots', hotspots=hotspots, clients=clients)