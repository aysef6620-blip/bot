import googleapiclient.discovery
from config import YOUTUBE_API_KEY, LIVE_CHAT_ID
import time

class YouTubeAPI:
    def __init__(self):
        self.youtube = googleapiclient.discovery.build(
            "youtube", "v3", developerKey=YOUTUBE_API_KEY
        )
        self.live_chat_id = LIVE_CHAT_ID
        self.processed_messages = set()
        
    def get_live_chat_messages(self):
        """Live chat'ten mesajları al"""
        try:
            request = self.youtube.liveChatMessages().list(
                liveChatId=self.live_chat_id,
                part="snippet",
                maxResults=2000
            )
            response = request.execute()
            return response.get('items', [])
        except Exception as e:
            print(f"❌ Live Chat mesajları alınamadı: {e}")
            return []
    
    def search_video(self, query):
        """YouTube'da video ara"""
        try:
            request = self.youtube.search().list(
                q=query,
                part="snippet",
                maxResults=1,
                type="video",
                videoDuration="medium"
            )
            response = request.execute()
            items = response.get('items', [])
            
            if items:
                video = items[0]
                return {
                    'id': video['id']['videoId'],
                    'title': video['snippet']['title'],
                    'channel': video['snippet']['channelTitle'],
                    'url': f"https://www.youtube.com/watch?v={video['id']['videoId']}"
                }
            return None
        except Exception as e:
            print(f"❌ Video arama hatası: {e}")
            return None
    
    def get_video_info(self, video_id):
        """Video bilgisini al (süre vb.)"""
        try:
            request = self.youtube.videos().list(
                id=video_id,
                part="contentDetails,snippet"
            )
            response = request.execute()
            items = response.get('items', [])
            
            if items:
                return items[0]
            return None
        except Exception as e:
            print(f"❌ Video bilgisi alınamadı: {e}")
            return None