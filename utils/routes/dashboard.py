

import hashlib, logging, random, re
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from flask import render_template, request, jsonify
from sqlalchemy import inspect, text
from sqlalchemy.dialects.postgresql import insert
from sqlmodel import select, func
from uuid import NAMESPACE_DNS, UUID, uuid5
from zoneinfo import ZoneInfo

from utils.database import get_session
from utils.models import Clients, Hotspots, Media, Subscribers, System_Users

logger = logging.getLogger(__name__)
    
from datetime import datetime, date
from sqlalchemy import func, cast, Date

class DashboardRoute:
    def __init__(self):
        pass

    def getall_hotspots(self) -> int:
        return get_session().execute(select(func.count(Hotspots.id))).scalar()


    def gettotal_connections(self) -> int:
        return get_session().execute(select(func.count(Subscribers.phone))).scalar()


    def getactive_connections(self) -> int:
        return get_session().execute(
            select(func.count(Subscribers.phone))
            .where(
                Subscribers.session_hour == func.date_trunc(
                    'hour', func.now().op('AT TIME ZONE')('Africa/Nairobi')
                )
            )
        ).scalar()


    def gethotspot_connections(self) -> list:
        rows = get_session().execute(
            select(Hotspots.name, func.count(Subscribers.id).label("total"))
            .join(Subscribers, Hotspots.id == Subscribers.hotspot_id, isouter=True)
            .group_by(Hotspots.id, Hotspots.name)
            .order_by(func.count(Subscribers.id).desc())
        ).all()
        return [{"name": r.name, "count": r.total} for r in rows]


    def gettotal_connections_today(self) -> int:
        return get_session().execute(
            select(func.count(Subscribers.phone))
            .where(cast(Subscribers.created_at, Date) == func.date(func.now().op('AT TIME ZONE')('Africa/Nairobi')))
        ).scalar()


    def getunique_connections_today(self) -> int:
        return get_session().execute(
            select(func.count(func.distinct(Subscribers.phone)))
            .where(cast(Subscribers.created_at, Date) == func.date(func.now().op('AT TIME ZONE')('Africa/Nairobi')))
        ).scalar()


    def getconnections_per_day(self) -> list:
        rows = get_session().execute(text("""
            SELECT TO_CHAR(created_at, 'Mon DD') AS date, COUNT(*) AS count 
            FROM subscribers
            WHERE created_at >= NOW() - INTERVAL '30 days'
            GROUP BY TO_CHAR(created_at, 'Mon DD')
            ORDER BY MIN(created_at)
        """)).all()
        return [{"date": r.date, "count": r.count} for r in rows]


    def getconnections_per_hour(self) -> list:
        rows = get_session().execute(text("""
            SELECT TO_CHAR(created_at, 'HH12 AM') AS hour, COUNT(*) AS count 
            FROM subscribers
            WHERE DATE(created_at) = CURRENT_DATE
            GROUP BY TO_CHAR(created_at, 'HH12 AM'), EXTRACT(HOUR FROM created_at)
            ORDER BY EXTRACT(HOUR FROM created_at)
        """)).all()
        return [{"hour": r.hour, "count": r.count} for r in rows]


    def getlatest_connections(self) -> list:
        rows = get_session().execute(text("""
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


    def __call__(self):
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
            "all_hotspots":             lambda: self.getall_hotspots(),
            "total_connections":        lambda: self.gettotal_connections(),
            "active_connections":       lambda: self.getactive_connections(),
            "hotspot_connections":      lambda: self.gethotspot_connections(),
            "total_connections_today":  lambda: self.gettotal_connections_today(),
            "unique_connections_today": lambda: self.getunique_connections_today(),
            "connections_per_day":      lambda: self.getconnections_per_day(),
            "connections_per_hour":     lambda: self.getconnections_per_hour(),
            "latest_connections":       lambda: self.getlatest_connections(),
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
