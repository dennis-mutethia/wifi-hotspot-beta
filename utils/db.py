import os, psycopg2
from dotenv import load_dotenv

class Video():
    def __init__(self, videoId, title, description, liveBroadcastContent, publishedAt):
        self.videoId = videoId
        self.title = title
        self.description = description 
        self.liveBroadcastContent = liveBroadcastContent
        self.publishedAt = publishedAt
    
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
            
    def get_videos(self, liveBroadcastContent='none', limit=5, current_page=1):
        offset = (current_page - 1) * limit
        self.ensure_connection()        
        query = """
        SELECT videoId, title, description, liveBroadcastContent, publishedAt
        FROM youtube_videos
        WHERE liveBroadcastContent = %s
        ORDER BY publishedAt DESC
        LIMIT %s OFFSET %s
        """
        params = [liveBroadcastContent, limit, offset]
                
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, tuple(params))
                data = cursor.fetchall()
                videos = []
                for datum in data:                    
                    videos.append(Video(datum[0], datum[1], datum[2], datum[3], datum[4]))

                return videos 
        except Exception as e:
            self.conn.rollback()
            raise e   
  
    def add_video(self, videoId, title, description, liveBroadcastContent, publishedAt):
        self.ensure_connection()            
        query = """
        INSERT INTO youtube_videos(videoId, title, description, liveBroadcastContent, publishedAt) 
        VALUES(%s, %s, %s, %s, %s)
        ON CONFLICT (videoId)
        DO UPDATE SET 
            title = EXCLUDED.title,
            description = EXCLUDED.description,
            liveBroadcastContent = EXCLUDED.liveBroadcastContent
        RETURNING videoId
        """

        params = (videoId, title, description, liveBroadcastContent, publishedAt)
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, tuple(params))
                self.conn.commit()
                row_id = cursor.fetchone()[0]
                return row_id
        except Exception as e:
            self.conn.rollback()
            raise e      