
class Client():
    def __init__(self, id, name, phone, background_color, foreground_color, hotspots):
        self.id = id
        self.name = name
        self.phone = phone
        self.background_color = background_color
        self.foreground_color = foreground_color
        self.hotspots = hotspots        

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'background_color': self.background_color,
            'foreground_color': self.foreground_color,
            'hotspots': self.hotspots
        }

class Hotspot():
    def __init__(self, id, name, hotspot_username, hotspot_password, client_id, client_name, subscribers):
        self.id = id
        self.name = name
        self.hotspot_username = hotspot_username
        self.hotspot_password = hotspot_password
        self.client_id = client_id
        self.client_name = client_name
        self.subscribers = subscribers     

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'hotspot_username': self.hotspot_username,
            'hotspot_password': self.hotspot_password,
            'client_id': self.client_id,
            'client_name': self.client_name,
            'subscribers': self.subscribers
        }
   
class Media():
    def __init__(self, id, type, source_id, client_id, hotspot_id):
        self.id = id
        self.type = type
        self.source_id = source_id
        self.client_id = client_id
        self.hotspot_id = hotspot_id     

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'source_id': self.source_id,
            'client_id': self.client_id,
            'hotspot_id': self.hotspot_id
        }

class Subscriber():
    def __init__(self, id, phone, session_hour, created_at, client, hotspot, device, ip_address, status=False):
        self.id = id
        self.phone = phone
        self.session_hour = session_hour
        self.created_at = created_at
        self.client = client
        self.hotspot = hotspot
        self.device = device
        self.ip_address = ip_address
        self.status = 'Connected' if status else 'Disconnected'