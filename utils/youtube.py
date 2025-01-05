import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

from utils.db import Db

load_dotenv()

class Youtube():
    def __init__(self):
        YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
        YOUTUBE_CHANNEL_HANDLE = os.getenv('YOUTUBE_CHANNEL_HANDLE')
        YOUTUBE_API_SERVICE_NAME = 'youtube'
        YOUTUBE_API_VERSION = 'v3'
        self.youtube_client = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=YOUTUBE_API_KEY)
        self.channel_id = self.get_channel_id_by_handle(YOUTUBE_CHANNEL_HANDLE)
        self.db = Db()
                
    def get_channel_id_by_handle(self, handle):
        try:
            # Search for the channel based on the handle
            request = self.youtube_client.search().list(
                part="snippet",
                q=handle,  # Searching using the handle or channel name
                type="channel",  # Specify that we want to search for channels
                maxResults=1  # Limit to 1 result
            )
            response = request.execute()

            # Check if 'items' is in the response
            if 'items' in response and len(response['items']) > 0:
                channel_id = response['items'][0]['snippet']['channelId']
                return channel_id
            else:
                print(f"No channel found for handle: {handle}")
                return None

        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    
     
    # Fetch the channel's videos
    def get_channel_videos(self, max_results=10):        
        # Fetch the latest videos from the channel
        video_response = self.youtube_client.search().list(
            part='snippet',
            channelId=self.channel_id,
            order='date',  # Order by the latest videos
            maxResults=max_results
        ).execute()

        videos = []
        for item in video_response['items']:
            videoId = item['id']['videoId']
            title = item['snippet']['title']
            description = item['snippet']['description']
            liveBroadcastContent = item['snippet']['liveBroadcastContent']
            publishedAt = item['snippet']['publishedAt']
            thumbnail = item['snippet']['thumbnails']['high']['url']
            videos.append(
                {
                    'videoId': videoId, 
                    'title': title, 
                    'description': description,
                    'liveBroadcastContent': liveBroadcastContent,
                    'publishedAt': publishedAt,
                    'thumbnail': thumbnail
                }
            )
        
        return videos

    # Fetch the live stream (if any) from the channel
    def get_live_video(self):        
        # Search for live stream videos for the channel
        search_response = self.youtube_client.search().list(
            part='snippet',
            channelId=self.channel_id,
            eventType='live',  # Only get live events
            type='video'  # Only videos (not playlists)
        ).execute()

        if search_response['items']:
            live_video = search_response['items'][0]
            live_video_id = live_video['id']['videoId']
            live_video_title = live_video['snippet']['title']
            return {'title': live_video_title, 'video_id': live_video_id}
        
        return None