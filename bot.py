#!/usr/bin/env python3
"""
YouTube Live Chat Music Request Bot
Canlı yayında izleyicilerin !sr komutuyla müzik isteyebilmesi
"""

import time
import threading
from youtube_api import YouTubeAPI
from music_player import MusicPlayer
from downloader import YouTubeDownloader
from config import FULL_COMMAND, YOUTUBE_API_KEY, LIVE_CHAT_ID

class YouTubeMusicBot:
    def __init__(self):
        print("🤖 Bot başlatılıyor...")
        
        # API kontrolü
        if not YOUTUBE_API_KEY or not LIVE_CHAT_ID:
            raise Exception("❌ YOUTUBE_API_KEY ve LIVE_CHAT_ID ayarlanmalı!")
        
        self.youtube_api = YouTubeAPI()
        self.music_player = MusicPlayer()
        self.downloader = YouTubeDownloader()
        self.processed_messages = set()
        self.user_requests = {}  # Kullanıcı başına istek sayısı
        
        print("✅ Bot hazır!")
        print(f"📝 Komut: {FULL_COMMAND}")
        print(f"💬 Live Chat ID: {LIVE_CHAT_ID}")
    
    def parse_command(self, message):
        """Komut ve argümanları ayıkla"""
        message = message.strip()
        if not message.startswith(FULL_COMMAND):
            return None, None
        
        parts = message[len(FULL_COMMAND):].strip().split(' ', 1)
        command = parts[0].lower() if parts else None
        args = parts[1] if len(parts) > 1 else None
        
        return command, args
    
    def handle_sr_command(self, song_query, username):
        """!sr komutunu işle"""
        if not song_query or len(song_query.strip()) < 2:
            print(f"⚠️ {username}: Geçersiz şarkı adı")
            return False
        
        # Rate limiting
        if username in self.user_requests:
            if self.user_requests[username] >= 3:  # Maksimum 3 istek
                print(f"⚠️ {username}: Çok fazla istek!")
                return False
        else:
            self.user_requests[username] = 0
        
        print(f"🔍 Aranıyor: {song_query}")
        
        # Videoyu ara
        video = self.youtube_api.search_video(song_query)
        if not video:
            print(f"❌ Video bulunamadı: {song_query}")
            return False
        
        print(f"✨ Bulundu: {video['title']}")
        
        # Ses indir
        file_path = self.downloader.download_audio(video['url'], video['title'])
        if not file_path:
            print(f"❌ İndirme başarısız")
            return False
        
        # Kuyruğa ekle
        track = {
            'title': video['title'],
            'channel': video['channel'],
            'url': video['url'],
            'path': file_path,
            'requested_by': username
        }
        
        if self.music_player.add_to_queue(track):
            self.user_requests[username] = self.user_requests.get(username, 0) + 1
            return True
        
        return False
    
    def handle_queue_command(self):
        """Kuyruk bilgisini göster"""
        info = self.music_player.get_queue_info()
        print("\n📋 KUYRUK BİLGİSİ")
        print("=" * 50)
        
        if info['current']:
            print(f"▶️ Çalıyor: {info['current']['title']}")
            print(f"   📺 Kanal: {info['current']['channel']}")
            print(f"   👤 İstek: {info['current']['requested_by']}")
        
        if info['next_tracks']:
            print(f"\n⏭️ Sıradakiler ({info['queue_size']} şarkı):")
            for i, track in enumerate(info['next_tracks'], 1):
                print(f"   {i}. {track['title']} - {track['requested_by']}")
        else:
            print("   (Boş)")
        print("=" * 50 + "\n")
    
    def monitor_chat(self):
        """Live chat'i izle"""
        print("\n👀 Chat izlenmeye başlandı...")
        error_count = 0
        
        while True:
            try:
                messages = self.youtube_api.get_live_chat_messages()
                
                for message in messages:
                    try:
                        snippet = message['snippet']
                        message_id = message['id']
                        
                        # Zaten işlenmiş mesajı geç
                        if message_id in self.processed_messages:
                            continue
                        
                        self.processed_messages.add(message_id)
                        
                        # Son 1000 mesajı sakla (RAM tasarrufu)
                        if len(self.processed_messages) > 1000:
                            self.processed_messages = set(list(self.processed_messages)[-1000:])
                        
                        # Yalnızca yayınlanan mesajları işle
                        if snippet['type'] != 'textMessageEvent':
                            continue
                        
                        message_text = snippet['displayMessage']
                        username = snippet['authorDisplayName']
                        
                        # Komut kontrolü
                        command, args = self.parse_command(message_text)
                        
                        if command == 'sr' or command == 'request':
                            print(f"💬 {username}: {message_text}")
                            self.handle_sr_command(args, username)
                        
                        elif command == 'queue' or command == 'q':
                            self.handle_queue_command()
                        
                        elif command == 'skip':
                            print(f"💬 {username}: !skip")
                            self.music_player.skip()
                        
                        elif command == 'pause':
                            print(f"💬 {username}: !pause")
                            self.music_player.pause()
                        
                        elif command == 'resume' or command == 'play':
                            print(f"💬 {username}: !resume")
                            self.music_player.resume()
                        
                        elif command == 'help':
                            print(f"\n📖 KOMUTLAR:")
                            print(f"  {FULL_COMMAND} <şarkı> - Müzik iste")
                            print(f"  {FULL_COMMAND}queue - Kuyruk göster")
                            print(f"  {FULL_COMMAND}skip - Atla")
                            print(f"  {FULL_COMMAND}pause - Duraklat")
                            print(f"  {FULL_COMMAND}resume - Devam et\n")
                    
                    except Exception as e:
                        print(f"⚠️ Mesaj işleme hatası: {e}")
                
                error_count = 0
                time.sleep(2)  # API rate limit için
            
            except Exception as e:
                error_count += 1
                print(f"❌ Chat hatası ({error_count}): {e}")
                if error_count > 5:
                    print("❌ Çok fazla hata, bot durduruldu")
                    break
                time.sleep(5)
    
    def run(self):
        """Botu çalıştır"""
        try:
            # Chat izleme thread'ini başlat
            chat_thread = threading.Thread(target=self.monitor_chat, daemon=True)
            chat_thread.start()
            
            # Ana thread aktif tut
            while True:
                time.sleep(1)
        
        except KeyboardInterrupt:
            print("\n\n👋 Bot kapatılıyor...")
        except Exception as e:
            print(f"❌ Bot hatası: {e}")

if __name__ == "__main__":
    try:
        bot = YouTubeMusicBot()
        bot.run()
    except Exception as e:
        print(f"❌ Başlatma hatası: {e}")