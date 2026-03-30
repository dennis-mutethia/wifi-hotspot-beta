import logging, random, re
from datetime import datetime
from flask import request, jsonify
from sqlalchemy import inspect, text
from sqlalchemy.dialects.postgresql import insert
from sqlmodel import select
from uuid import NAMESPACE_DNS, UUID, uuid5
from zoneinfo import ZoneInfo

from utils.database import get_session
from utils.models import Clients, Hotspots, Media, Subscribers

logger = logging.getLogger(__name__)

def to_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}

def portal_data(hotspot_id: str):
    try:
        hotspot_id = UUID(hotspot_id)
        session = get_session()

        # Fetch hotspot + client in one query
        stmt = (
            select(Hotspots, Clients)
            .join(Clients, Hotspots.client_id == Clients.id)
            .where(Hotspots.id == hotspot_id)
        )
        row = session.execute(stmt).one_or_none()

        if not row:
            logger.warning(f"No data found for hotspot_id: {hotspot_id}")
            return jsonify({"error": "Hotspot not found"}), 404

        hotspot, client = row

        # Fetch media separately
        media = session.execute(
            select(Media).where(
                Media.hotspot_id == hotspot.id,
                Media.client_id == client.id
            )
        ).scalars().all()

        logger.info(f"Fetched hotspot_id: {hotspot_id} - Client: {client.name}, Media count: {len(media)}")

        images = [m for m in media if m.type == 'image']
        videos = [m for m in media if m.type == 'video']

        return jsonify({
            "client": to_dict(client),
            "video": to_dict(random.choice(videos)) if videos else None,
            "images": [to_dict(i) for i in random.sample(images, min(5, len(images)))]
        }), 200

    except Exception as e:
        logger.error(f"Error in portal_data for hotspot_id {hotspot_id}: {e}")
        return jsonify({"error": "Internal server error"}), 500

def get_next_user_id(session) -> int:
    result = session.execute(text("SELECT nextval('subscribers_user_id_seq')")).scalar()
    return result

def subscribe(hotspot_id):
    try:
        hotspot_id = UUID(hotspot_id)
        session = get_session()
        phone = request.form['phone']

        hotspot = session.execute(
            select(Hotspots).where(Hotspots.id == hotspot_id)
        ).scalar_one_or_none()

        if not hotspot:
            return jsonify({"error": "Hotspot not found"}), 404

        # Get device info from User-Agent
        user_agent = request.headers.get('User-Agent', '')
        match = re.search(r'\(([^)]+)\)', user_agent)
        device_parts = match.group(1).split(';') if match else []

        if len(device_parts) == 2:
            device = f"{device_parts[0].strip()} {device_parts[1].strip()}"
        elif len(device_parts) > 2:
            device = f"{device_parts[2].strip()} {device_parts[1].strip()}"
        else:
            device = 'Unknown Device'
        
        session_hour = datetime.now(ZoneInfo("Africa/Nairobi")).replace(minute=0, second=0, microsecond=0, tzinfo=None)
        
        subscriber_id = uuid5(NAMESPACE_DNS, f'{phone}-{session_hour}-{hotspot_id}')
        
        stmt = insert(Subscribers).values(
            id=subscriber_id,
            phone=phone,
            user_id=get_next_user_id(session),
            session_hour=session_hour,
            client_id=hotspot.client_id,
            hotspot_id=hotspot_id,
            device=device,
            created_at=datetime.now(ZoneInfo("Africa/Nairobi")).replace(tzinfo=None)
        ).on_conflict_do_nothing(index_elements=['id'])

        session.execute(stmt)
        session.commit()

        subscriber = session.execute(
            select(Subscribers).where(Subscribers.id == subscriber_id)
        ).scalar_one()

        return jsonify({
            "username": f"user-{subscriber.user_id % 249}",
            "password": "TgdV84"
        }), 200

    except Exception as e:
        logger.error(f"Error in subscribe for hotspot_id {hotspot_id}: {e}")
        return jsonify({"error": "Internal server error"}), 500