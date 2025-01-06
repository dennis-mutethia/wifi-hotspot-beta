
class Client():
    def __init__(self, id, name, background_color, foreground_color):
        self.id = id
        self.name = name
        self.background_color = background_color
        self.foreground_color = foreground_color

class Station():
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