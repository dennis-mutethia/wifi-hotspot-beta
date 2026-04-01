
import logging
from flask import render_template, request, jsonify
from sqlmodel import select, func
from uuid import UUID

from utils.database import get_session
from utils.helper import hash_password
from utils.models import Clients, System_Users

logger = logging.getLogger(__name__)
    

class SystemUsersRoute:
    def __init__(self):
        pass

    def __call__(self):  
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

        except Exception as e:
            logger.error(f"Error in system_users: {e}")
            system_users, clients = [], []
        
        finally:
            try:
                system_users = session.execute(select(System_Users).order_by(System_Users.name)).scalars().all()
                clients = session.execute(select(Clients).order_by(Clients.name)).scalars().all()
                session.close()
                
            except Exception as e:
                logger.error(f"Error closing session in system_users: {e}")

        return render_template('system-users.html', page='system_users', system_users=system_users, clients=clients)