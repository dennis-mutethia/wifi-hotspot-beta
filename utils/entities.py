
class Client():
    def __init__(self, id, name, phone, background_color, foreground_color, hotspots):
        self.id = id
        self.name = name
        self.phone = phone
        self.background_color = background_color
        self.foreground_color = foreground_color
        self.hotspots = hotspots

class Hotspot():
    def __init__(self, id, name, hotspot_username, hotspot_password, client_id, client_name, subscribers):
        self.id = id
        self.name = name
        self.hotspot_username = hotspot_username
        self.hotspot_password = hotspot_password
        self.client_id = client_id
        self.client_name = client_name
        self.subscribers = subscribers
      
class Video():
    def __init__(self, video_id, video_title):
        self.video_id = video_id
        self.video_title = video_title

class Image():
    def __init__(self, image_id):
        self.image_id = image_id

class Subscriber():
    def __init__(self, id, phone, session_hour, created_at, client, hotspot):
        self.id = id
        self.phone = phone
        self.session_hour = session_hour
        self.created_at = created_at
        self.client = client
        self.hotspot = hotspot