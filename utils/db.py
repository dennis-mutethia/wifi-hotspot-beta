import os, psycopg2
from dotenv import load_dotenv

from utils.entities import Client, Image, Station, Video
    
class Db():
    def __init__(self):
        load_dotenv()
        # Access the environment variables
        self.conn_params = {
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT'),
            'database': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD')
        }
        
        self.conn = None
        self.ensure_connection()
    
    def ensure_connection(self):
        try:
            # Check if the connection is open
            if self.conn is None or self.conn.closed:
                self.conn = psycopg2.connect(**self.conn_params)
            else:
                # Test the connection
                with self.conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
        except Exception:
            # Reconnect if the connection is invalid
            self.conn = psycopg2.connect(**self.conn_params)  
            
    def get_client(self, id=0):  
        self.ensure_connection()          
        query = """
        SELECT id, name, background_color, foreground_color
        FROM clients
        WHERE id=%s
        """
        params = [id]
                
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, tuple(params))
                data = cursor.fetchone()
                if data is not None:
                    return Client(data[0], data[1], data[2], data[3])
            
        except Exception as e:
            self.conn.rollback()
            raise e   
            
    def get_station(self, id=0):  
        self.ensure_connection()          
        query = """
        SELECT id, name, hotspot_username, hotspot_password, client_id
        FROM stations
        WHERE id=%s
        """
        params = [id]
                
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, tuple(params))
                data = cursor.fetchone()
                if data is not None:
                    client = self.get_client(id=data[4])
                        
                    return Station(data[0], data[1], data[2], data[3], client)
            
        except Exception as e:
            self.conn.rollback()
            raise e   
            
    def get_videos(self, station):  
        self.ensure_connection()        
        query = """
        SELECT video_id, video_title, published_at
        FROM youtube_videos
        WHERE station_id=%s
        """
        params = [station.id]
                
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, tuple(params))
                data = cursor.fetchall()
                
                if len(data) == 0:
                    query = f'{query} OR client_id=%s'
                    params.append(station.client.id)
                    cursor.execute(query, tuple(params))
                    data = cursor.fetchall()
                    
                videos = []
                for datum in data:                    
                    videos.append(Video(datum[0], datum[1], datum[2]))

                return videos 
        except Exception as e:
            self.conn.rollback()
            raise e   
  
    def add_video(self, video_id, video_title, published_at, client_id, station_id):
        self.ensure_connection()            
        query = """
        INSERT INTO youtube_videos(video_id, video_title, published_at, client_id, station_id) 
        VALUES(%s, %s, %s, %s, %s)
        ON CONFLICT (video_id, station_id)
        DO UPDATE SET 
            video_title = EXCLUDED.video_title
        RETURNING videoId
        """

        params = (video_id, video_title, published_at, client_id, station_id)
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, tuple(params))
                self.conn.commit()
                row_id = cursor.fetchone()[0]
                return row_id
        except Exception as e:
            self.conn.rollback()
            raise e      
            
    def get_images(self, station):  
        self.ensure_connection()        
        query = """
        SELECT image_id
        FROM postimg_images
        WHERE station_id=%s
        """
        params = [station.id]
                
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, tuple(params))
                data = cursor.fetchall()
                
                if len(data) == 0:
                    query = f'{query} OR client_id=%s'
                    params.append(station.client.id)
                    cursor.execute(query, tuple(params))
                    data = cursor.fetchall()
                    
                images = []
                for datum in data:                    
                    images.append(Image(datum[0]))

                return images 
        except Exception as e:
            self.conn.rollback()
            raise e   