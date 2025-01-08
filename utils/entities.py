
class Client():
    def __init__(self, id, name, phone, background_color, foreground_color, hotspots):
        self.id = id
        self.name = name
        self.phone = phone
        self.background_color = background_color
        self.foreground_color = foreground_color
        self.hotspots = hotspots

class Hotspot():
    def __init__(self, id, name, hotspot_username, hotspot_password, client):
        self.id = id
        self.name = name
        self.hotspot_username = hotspot_username
        self.hotspot_password = hotspot_password
        self.client = client
      
class Video():
    def __init__(self, video_id, video_title, published_at):
        self.video_id = video_id
        self.video_title = video_title
        self.published_at = published_at

class Image():
    def __init__(self, image_id):
        self.image_id = image_id

class HotspotUser():
    def __init__(self, id, phone, session_hour, created_at, client, hotspot):
        self.id = id
        self.phone = phone
        self.session_hour = session_hour
        self.created_at = created_at
        self.client = client
        self.hotspot = hotspot