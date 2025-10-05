import os, psycopg2
from dotenv import load_dotenv

from utils.entities import Client, Image, Hotspot, Video
    
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
        except Exception as e:
            # Reconnect if the connection is invalid
            self.conn = psycopg2.connect(**self.conn_params)  
            raise e   
        
  
    def update_client(self, id, name, phone, background_color, foreground_color):
        self.ensure_connection()            
        
        query = f"""
        INSERT INTO clients(name, phone, background_color, foreground_color, created_at {',id' if id else ''}) 
        VALUES(%s, %s, %s, %s, CURRENT_TIMESTAMP AT TIME ZONE 'Africa/Nairobi' {',%s' if id else ''})
        ON CONFLICT (id)
        DO UPDATE SET 
            name = EXCLUDED.name, 
            phone = EXCLUDED.phone, 
            background_color = EXCLUDED.background_color, 
            foreground_color = EXCLUDED.foreground_color
        RETURNING id
        """
        params = [name, phone, background_color, foreground_color]
        if id:
            params.append(id)
                    
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, tuple(params))
                self.conn.commit()
                row_id = cursor.fetchone()[0]
                return row_id
        except Exception as e:
            self.conn.rollback()
            raise e
            
                         
    def get_clients(self, id=0):  
        self.ensure_connection()          
        query = """
        WITH hotspots AS(
            SELECT client_id, COUNT(id) AS count
            FROM hotspots 
            GROUP BY client_id
        )
        SELECT id, name, phone, background_color, foreground_color, hotspots.count AS hotspots
        FROM clients
        LEFT JOIN hotspots ON hotspots.client_id = clients.id
        WHERE 1=1
        """
        params = []
        if id>0:
            query = f"{query} AND id=%s"            
            params.append(id)
                
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, tuple(params))
                data = cursor.fetchall()
                clients = []
                for datum in data:  
                    client = Client(datum[0], datum[1], datum[2], datum[3], datum[4], datum[5])
                    clients.append(client)
                    
                return clients
            
        except Exception as e:
            self.conn.rollback()
            raise e       
        
        
    def remove_client(self, id):
        self.ensure_connection()    
        query = """
        DELETE FROM clients
        WHERE id = %s
        """
        params = [id]
        
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, tuple(params))
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        
            
    def get_hotspots(self, id=0, client_id=0):  
        self.ensure_connection()          
        query = """        
        WITH subscribers AS(
            SELECT hotspot_id, COUNT(id) AS count
            FROM hotspot_users 
            GROUP BY hotspot_id
        )
        SELECT hotspots.id, hotspots.name, hotspot_username, hotspot_password, clients.id, clients.name, subscribers.count
        FROM hotspots 
        INNER JOIN clients ON clients.id = hotspots.client_id
        LEFT JOIN subscribers ON subscribers.hotspot_id = hotspots.id 
        WHERE 1=1      
        """
        params = []
        if id>0:
            query = f"{query} AND hotspots.id=%s"            
            params.append(id)
        if client_id>0:
            query = f"{query} AND hotspots.client_id=%s"            
            params.append(client_id)
                
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, tuple(params))
                data = cursor.fetchall()
                hotspots = []
                for datum in data:  
                    hotspot = Hotspot(datum[0], datum[1], datum[2], datum[3], datum[4], datum[5], datum[6])
                    hotspots.append(hotspot)
                    
                return hotspots
            
        except Exception as e:
            self.conn.rollback()
            raise e     
                
  
    def update_hotspot(self, id, name, hotspot_username, hotspot_password, client_id):
        self.ensure_connection()            
        
        query = f"""
        INSERT INTO hotspots(name, hotspot_username, hotspot_password, client_id, created_at {',id' if id else ''}) 
        VALUES(%s, %s, %s, %s, CURRENT_TIMESTAMP AT TIME ZONE 'Africa/Nairobi' {',%s' if id else ''})
        ON CONFLICT (id)
        DO UPDATE SET 
            name = EXCLUDED.name, 
            hotspot_username = EXCLUDED.hotspot_username, 
            hotspot_password = EXCLUDED.hotspot_password, 
            client_id = EXCLUDED.client_id
        RETURNING id
        """
        params = [name, hotspot_username, hotspot_password, client_id]
        if id:
            params.append(id)
                    
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, tuple(params))
                self.conn.commit()
                row_id = cursor.fetchone()[0]
                return row_id
        except Exception as e:
            self.conn.rollback()
            raise e
        
        
    def remove_hotspot(self, id):
        self.ensure_connection()    
        query = """
        DELETE FROM hotspots
        WHERE id = %s
        """
        params = [id]
        
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, tuple(params))
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        
                    
    def get_videos(self, hotspot):  
        self.ensure_connection()        
        query = """
        SELECT video_id, video_title, published_at
        FROM youtube_videos
        WHERE hotspot_id=%s
        """
        params = [hotspot.id]
                
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, tuple(params))
                data = cursor.fetchall()
                
                if len(data) == 0:
                    query = f'{query} OR client_id=%s'
                    params.append(hotspot.client.id)
                    cursor.execute(query, tuple(params))
                    data = cursor.fetchall()
                    
                videos = []
                for datum in data:                    
                    videos.append(Video(datum[0], datum[1], datum[2]))

                return videos 
        except Exception as e:
            self.conn.rollback()
            raise e   
        
  
    def add_video(self, video_id, video_title, published_at, client_id, hotspot_id):
        self.ensure_connection()            
        query = """
        INSERT INTO youtube_videos(video_id, video_title, published_at, client_id, hotspot_id) 
        VALUES(%s, %s, %s, %s, %s)
        ON CONFLICT (video_id, hotspot_id)
        DO UPDATE SET 
            video_title = EXCLUDED.video_title
        RETURNING id
        """

        params = (video_id, video_title, published_at, client_id, hotspot_id)
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, tuple(params))
                self.conn.commit()
                row_id = cursor.fetchone()[0]
                return row_id
        except Exception as e:
            self.conn.rollback()
            raise e  
            
            
    def get_images(self, hotspot):  
        self.ensure_connection()        
        query = """
        SELECT image_id
        FROM postimg_images
        WHERE hotspot_id=%s
        """
        params = [hotspot.id]
                
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, tuple(params))
                data = cursor.fetchall()
                
                if len(data) == 0:
                    query = f'{query} OR client_id=%s'
                    params.append(hotspot.client.id)
                    cursor.execute(query, tuple(params))
                    data = cursor.fetchall()
                    
                images = []
                for datum in data:                    
                    images.append(Image(datum[0]))

                return images 
        except Exception as e:
            self.conn.rollback()
            raise e 
          
  
    def add_hotspot_user(self, phone, hotspot_id, client_id):
        self.ensure_connection()            
        query = """
        INSERT INTO hotspot_users(phone, hotspot_id, client_id, session_hour, created_at) 
        VALUES(%s, %s, %s, DATE_TRUNC('hour', CURRENT_TIMESTAMP AT TIME ZONE 'Africa/Nairobi'), CURRENT_TIMESTAMP AT TIME ZONE 'Africa/Nairobi')
        ON CONFLICT (phone, session_hour, hotspot_id)
        DO NOTHING 
        RETURNING id
        """

        params = (phone, hotspot_id, client_id)
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, tuple(params))
                self.conn.commit()
                added = cursor.fetchone()
                row_id = added[0] if added is not None else 0
                return row_id
        except Exception as e:
            self.conn.rollback()
            raise e   
         
            
    def get_connection_counts_per_hotspot(self):  
        self.ensure_connection()        
        query = """
        WITH subs AS(
            SELECT hotspot_id, COUNT(*) AS count 
            FROM hotspot_users
            GROUP BY hotspot_id
        )
        SELECT hotspots.name, subs.count
        FROM hotspots
        INNER JOIN subs ON subs.hotspot_id = hotspots.id
        """
                
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query,)
                data = cursor.fetchall()
                                    
                counts = []
                for datum in data:  
                    count = {
                        'name' : datum[0],
                        'count' : datum[1]
                    }                  
                    counts.append(count)

                return counts 
        except Exception as e:
            self.conn.rollback()
            raise e  
                 
            
    def get_total_connections(self, today=False, active=False):  
        self.ensure_connection()        
        query = """
        SELECT COUNT(phone) AS count 
        FROM hotspot_users
        WHERE 1=1
        """
        
        if today:
            query = f"{query} AND DATE(created_at) = DATE(CURRENT_TIMESTAMP AT TIME ZONE 'Africa/Nairobi')"
        if active:
            query = f"{query} AND session_hour = DATE_TRUNC('hour', CURRENT_TIMESTAMP AT TIME ZONE 'Africa/Nairobi')"
                
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchone()
                return result[0] if result else 0
        except Exception as e:
            self.conn.rollback()
            raise e 
                
            
    def get_unique_connections(self, today=False):  
        self.ensure_connection()        
        query = """
        SELECT COUNT(DISTINCT phone) AS count 
        FROM hotspot_users
        WHERE 1=1
        """
        
        if today:
            query = f"{query} AND DATE(created_at) = DATE(CURRENT_TIMESTAMP AT TIME ZONE 'Africa/Nairobi')"
                
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchone()
                return result[0] if result else 0
        except Exception as e:
            self.conn.rollback()
            raise e
            
            
    def get_latest_connections(self):  
        self.ensure_connection()        
        query = """
        WITH subs AS(
            SELECT phone, hotspot_id, TO_CHAR(created_at, 'Mon DD HH24:MI:SS') AS created_at, session_hour = DATE_TRUNC('hour', CURRENT_TIMESTAMP AT TIME ZONE 'Africa/Nairobi') AS active
            FROM hotspot_users
            ORDER BY created_at DESC
            LIMIT 5
        )
        SELECT subs.phone, hotspots.name, subs.created_at, subs.active
        FROM hotspots
        INNER JOIN subs ON subs.hotspot_id = hotspots.id
        """
                
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query,)
                data = cursor.fetchall()
                                    
                subs = []
                for datum in data:  
                    sub = {
                        'phone' : datum[0],
                        'hotspot' : datum[1],
                        'datetime' : datum[2],
                        'active' : datum[3]
                    }                  
                    subs.append(sub)

                return subs 
        except Exception as e:
            self.conn.rollback()
            raise e       
            
            
    def get_connections_per_day(self):  
        self.ensure_connection()        
        query = """
        SELECT TO_CHAR(created_at, 'Mon DD') AS date, COUNT(*) AS count 
        FROM hotspot_users
        WHERE created_at >= NOW() - INTERVAL '30 days'
        GROUP BY TO_CHAR(created_at, 'Mon DD')
        ORDER BY TO_CHAR(created_at, 'Mon DD')
        """
                
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query,)
                data = cursor.fetchall()
                                    
                subs = []
                for datum in data:  
                    sub = {
                        'date' : datum[0],
                        'count' : datum[1]
                    }                  
                    subs.append(sub)

                return subs 
        except Exception as e:
            self.conn.rollback()
            raise e   
            