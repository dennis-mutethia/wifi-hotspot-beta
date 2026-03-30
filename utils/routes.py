
import hashlib, logging, random, re
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from flask import render_template, request, jsonify
from sqlalchemy import inspect, text
from sqlalchemy.dialects.postgresql import insert
from sqlmodel import select, func
from uuid import NAMESPACE_DNS, UUID, uuid5

from utils.database import get_session
from utils.models import Clients, Hotspots, Media, Subscribers, System_Users

logger = logging.getLogger(__name__)

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
from datetime import datetime, date
from sqlalchemy import func, cast, Date


def to_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


def _get_all_hotspots(session) -> int:
    return session.execute(select(func.count(Hotspots.id))).scalar()


def _get_total_connections(session) -> int:
    return session.execute(select(func.count(Subscribers.phone))).scalar()


def _get_active_connections(session) -> int:
    return session.execute(
        select(func.count(Subscribers.phone))
        .where(
            Subscribers.session_hour == func.date_trunc(
                'hour', func.now().op('AT TIME ZONE')('Africa/Nairobi')
            )
        )
    ).scalar()


def _get_hotspot_connections(session) -> list:
    rows = session.execute(
        select(Hotspots.name, func.count(Subscribers.id).label("total"))
        .join(Subscribers, Hotspots.id == Subscribers.hotspot_id, isouter=True)
        .group_by(Hotspots.id, Hotspots.name)
        .order_by(func.count(Subscribers.id).desc())
    ).all()
    return [{"name": r.name, "count": r.total} for r in rows]


def _get_total_connections_today(session) -> int:
    return session.execute(
        select(func.count(Subscribers.phone))
        .where(cast(Subscribers.created_at, Date) == func.date(func.now().op('AT TIME ZONE')('Africa/Nairobi')))
    ).scalar()


def _get_unique_connections_today(session) -> int:
    return session.execute(
        select(func.count(func.distinct(Subscribers.phone)))
        .where(cast(Subscribers.created_at, Date) == func.date(func.now().op('AT TIME ZONE')('Africa/Nairobi')))
    ).scalar()


def _get_connections_per_day(session) -> list:
    rows = session.execute(text("""
        SELECT TO_CHAR(created_at, 'Mon DD') AS date, COUNT(*) AS count 
        FROM subscribers
        WHERE created_at >= NOW() - INTERVAL '30 days'
        GROUP BY TO_CHAR(created_at, 'Mon DD')
        ORDER BY MIN(created_at)
    """)).all()
    return [{"date": r.date, "count": r.count} for r in rows]


def _get_connections_per_hour(session) -> list:
    rows = session.execute(text("""
        SELECT TO_CHAR(created_at, 'HH12 AM') AS hour, COUNT(*) AS count 
        FROM subscribers
        WHERE DATE(created_at) = CURRENT_DATE
        GROUP BY TO_CHAR(created_at, 'HH12 AM'), EXTRACT(HOUR FROM created_at)
        ORDER BY EXTRACT(HOUR FROM created_at)
    """)).all()
    return [{"hour": r.hour, "count": r.count} for r in rows]


def _get_latest_connections(session) -> list:
    rows = session.execute(text("""
        WITH subs AS (
            SELECT phone, hotspot_id, TO_CHAR(created_at, 'Mon DD HH24:MI:SS') AS created_at,
                   session_hour = DATE_TRUNC('hour', CURRENT_TIMESTAMP AT TIME ZONE 'Africa/Nairobi') AS active
            FROM subscribers
            ORDER BY created_at DESC
            LIMIT 5
        )
        SELECT subs.phone, hotspots.name, subs.created_at, subs.active
        FROM hotspots
        INNER JOIN subs ON subs.hotspot_id = hotspots.id
    """)).all()
    return [{"phone": r.phone, "hotspot": r.name, "datetime": r.created_at, "active": r.active} for r in rows]


def dashboard():
    stats = {
        "all_hotspots": 0,
        "total_connections": 0,
        "active_connections": 0,
        "hotspot_connections": [],
        "total_connections_today": 0,
        "unique_connections_today": 0,
        "connections_per_day": [],
        "connections_per_hour": [],
        "latest_connections": []
    }

    tasks = {
        "all_hotspots":             lambda: _get_all_hotspots(get_session()),
        "total_connections":        lambda: _get_total_connections(get_session()),
        "active_connections":       lambda: _get_active_connections(get_session()),
        "hotspot_connections":      lambda: _get_hotspot_connections(get_session()),
        "total_connections_today":  lambda: _get_total_connections_today(get_session()),
        "unique_connections_today": lambda: _get_unique_connections_today(get_session()),
        "connections_per_day":      lambda: _get_connections_per_day(get_session()),
        "connections_per_hour":     lambda: _get_connections_per_hour(get_session()),
        "latest_connections":       lambda: _get_latest_connections(get_session()),
    }

    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(fn): key for key, fn in tasks.items()}
        for future in as_completed(futures):
            key = futures[future]
            try:
                stats[key] = future.result()
            except Exception as e:
                logger.error(f"Error fetching {key}: {e}")

    return render_template('dashboard.html', page='dashboard', **stats)                   
     

def clients():
    session = get_session()
    try:
        if request.method == 'POST':
            action = request.form['action']
            if action in ['add', 'edit']:
                name = request.form['clientName']
                phone = request.form['clientPhone']
                background_color = request.form['backgroundColor']
                foreground_color = request.form['foregroundColor']

                if action == 'add':
                    client = Clients(
                        name=name,
                        phone=phone,
                        background_color=background_color,
                        foreground_color=foreground_color
                    )
                    session.add(client)

                elif action == 'edit':
                    client_id = UUID(request.form['editClientId'])
                    client = session.execute(
                        select(Clients).where(Clients.id == client_id)
                    ).scalar_one()
                    client.name = name
                    client.phone = phone
                    client.background_color = background_color
                    client.foreground_color = foreground_color

            elif action == 'remove':
                client_id = UUID(request.form['removeClientId'])
                client = session.execute(
                    select(Clients).where(Clients.id == client_id)
                ).scalar_one()
                session.delete(client)

            session.commit()

        rows = session.execute(
            select(Clients, func.count(Hotspots.id).label("hotspots"))
            .join(Hotspots, Clients.id == Hotspots.client_id, isouter=True)
            .group_by(Clients.id)
            .order_by(Clients.name)
        ).all()
        
        clients = [
        {
            "id": c.id,
            "name": c.name,
            "phone": c.phone,
            "foreground_color": c.foreground_color,
            "background_color": c.background_color,
            "hotspots": count or 0,
        }
        for c, count in rows
    ]

        logger.info(f"Fetched clients: {len(clients)}")

    except Exception as e:
        logger.error(f"Error in clients: {e}")
        clients = []

    return render_template('clients.html', page='clients', clients=clients)


def hotspots():
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

        clients = session.execute(select(Clients).order_by(Clients.name)).scalars().all()
        #hotspots = session.execute(select(Hotspots).order_by(Hotspots.name)).scalars().all()
        
        rows = session.execute(
            select(Hotspots, func.count(Subscribers.id).label("subscribers"))
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

    except Exception as e:
        logger.error(f"Error in hotspots: {e}")
        hotspots, clients = [], []

    return render_template('hotspots.html', page='hotspots', hotspots=hotspots, clients=clients)


def subscribers():
    session = get_session()
    try:
        subscribers = session.execute(
            select(Subscribers).order_by(Subscribers.created_at.desc())
        ).scalars().all()
    except Exception as e:
        logger.error(f"Error in subscribers: {e}")
        subscribers = []

    return render_template('subscribers.html', page='subscribers', subscribers=subscribers)


def gallery():
    session = get_session()
    try:
        if request.method == 'POST':
            action = request.form['action']
            if action in ['add', 'edit']:
                source = request.form['source']
                client_id = UUID(request.form['clientId'])
                hotspot_id = UUID(request.form['hotspotId'])

                if 'youtube' in source:
                    media_type = 'video'
                    source = source
                elif 'postimg' in source:
                    media_type = 'image'
                    source = source
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

        hotspot_id = request.args.get('hotspotId', None)
        hotspot_id = UUID(hotspot_id) if hotspot_id else None

        media_query = select(Media)
        if hotspot_id:
            media_query = media_query.where(Media.hotspot_id == hotspot_id)

        media = session.execute(media_query).scalars().all()
        images = [m for m in media if m.type == 'image']
        videos = [m for m in media if m.type == 'video']
        hotspots = session.execute(select(Hotspots).order_by(Hotspots.name)).scalars().all()
        clients = session.execute(select(Clients).order_by(Clients.name)).scalars().all()

    except Exception as e:
        logger.error(f"Error in gallery: {e}")
        images, videos, hotspots, clients = [], [], [], []
        hotspot_id = None

    return render_template('gallery.html', page='gallery', hotspots=hotspots, clients=clients,
                           images=images, videos=videos, hotspot_id=hotspot_id)


def system_users():
    session = get_session()
    try:
        if request.method == 'POST':
            action = request.form['action']
            if action in ['add', 'edit']:
                name = request.form['systemUserName'].upper()
                phone = request.form['phone']
                client_id = UUID(request.form['clientId'])

                if action == 'add':
                    user = System_Users(name=name, phone=phone, client_id=client_id, password=hash_password(phone))
                    session.add(user)

                elif action == 'edit':
                    user_id = UUID(request.form['editSystemUserId'])
                    user = session.execute(
                        select(System_Users).where(System_Users.id == user_id)
                    ).scalar_one()
                    user.name = name
                    user.phone = phone
                    user.client_id = client_id

            elif action == 'remove':
                user_id = UUID(request.form['removeSystemUserId'])
                user = session.execute(
                    select(System_Users).where(System_Users.id == user_id)
                ).scalar_one()
                session.delete(user)

            session.commit()

        system_users = session.execute(select(System_Users).order_by(System_Users.name)).scalars().all()
        clients = session.execute(select(Clients).order_by(Clients.name)).scalars().all()

    except Exception as e:
        logger.error(f"Error in system_users: {e}")
        system_users, clients = [], []

    return render_template('system-users.html', page='system_users', system_users=system_users, clients=clients)