
import logging
from flask import render_template, request, jsonify
from sqlmodel import select, func
from uuid import UUID

from utils.database import get_session
from utils.models import Clients, Hotspots

logger = logging.getLogger(__name__)
    

class ClientsRoute:
    def __init__(self):
        pass

    def __call__(self):
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

        except Exception as e:
            logger.error(f"Error saving client: {e}")
            clients = []
            
        finally:
            try:
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
                
                session.close()
            except Exception as e:
                logger.error(f"Error closing session in clients: {e}")

        return render_template('clients.html', page='clients', clients=clients)