
import logging
from datetime import datetime
from zoneinfo import ZoneInfo
from flask import render_template, request, jsonify
from sqlmodel import select, func
from uuid import UUID

from utils.database import get_session
from utils.models import Clients, Hotspots, Subscribers

logger = logging.getLogger(__name__)
    

class SubscribersRoute:
    def __init__(self):
        pass

    def __call__(self):  
        session = get_session()
        try:
            rows = session.execute(
                select(
                    Subscribers,
                    Hotspots.name.label("hotspot_name"),
                    Clients.name.label("client_name")
                )
                .join(Hotspots, Hotspots.id == Subscribers.hotspot_id)
                .join(Clients, Clients.id == Hotspots.client_id)            
                .order_by(Subscribers.created_at.desc())
            ).all()
            
            
            subscribers = [
                {
                    "created_at": s.created_at,
                    "phone": s.phone,
                    "device": s.device,
                    "hotspot_name": hotspot_name,
                    "client_name": client_name,
                    "status": 'Connected' if s.session_hour == datetime.now(ZoneInfo("Africa/Nairobi")).replace(minute=0, second=0, microsecond=0, tzinfo=None) else 'Disconnected'
                }
                for s, hotspot_name, client_name in rows
            ]
            
        except Exception as e:
            logger.error(f"Error in subscribers: {e}")
            subscribers = []

        return render_template('subscribers.html', page='subscribers', subscribers=subscribers)