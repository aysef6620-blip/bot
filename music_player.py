import pygame
import os
from queue import Queue
from threading import Thread
import time

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.queue = Queue()
        self.current_track = None
        self.is_playing = False
        self.volume = 0.7
        self.player_thread = Thread(target=self._player_loop, daemon=True)
        self.player_thread.start()
    
    def _player_loop(self):
        """Müzik çalma döngüsü"""
        while True:
            try:
                if not self.is_playing and not self.queue.empty():
                    track = self.queue.get()
                    self.current_track = track
                    self.play_track(track['path'])
                time.sleep(0.1)
            except Exception as e:
                print(f"❌ Player hatası: {e}")
    
    def play_track(self, file_path):
        """Müzik çal"""
        try:
            if not os.path.exists(file_path):
                print(f"❌ Dosya bulunamadı: {file_path}")
                return False
            
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play()
            self.is_playing = True
            
            print(f"▶️ Çalıyor: {self.current_track['title']}")
            
            # Müzik bitene kadar bekle
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            self.is_playing = False
            return True
        except Exception as e:
            print(f"❌ Müzik çalma hatası: {e}")
            self.is_playing = False
            return False
    
    def add_to_queue(self, track):
        """Kuyruğa şarkı ekle"""
        if self.queue.qsize() < 50:  # Max 50 şarkı
            self.queue.put(track)
            print(f"➕ Kuyruğa eklendi: {track['title']} (Sıra: {self.queue.qsize()})")
            return True
        else:
            print("❌ Kuyruk dolu!")
            return False
    
    def skip(self):
        """Mevcut şarkıyı geç"""
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            print("⏭️ Şarkı atlandı")
    
    def pause(self):
        """Duraklat"""
        if self.is_playing:
            pygame.mixer.music.pause()
            print("⏸️ Duraklatıldı")
    
    def resume(self):
        """Devam et"""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.unpause()
            print("▶️ Devam ediyor")
    
    def set_volume(self, level):
        """Ses seviyesi ayarla (0-100)"""
        self.volume = max(0, min(1, level / 100))
        pygame.mixer.music.set_volume(self.volume)
        print(f"🔊 Ses: {int(self.volume * 100)}%")
    
    def get_queue_info(self):
        """Kuyruk bilgisini al"""
        queue_items = list(self.queue.queue)
        return {
            'current': self.current_track,
            'queue_size': len(queue_items),
            'next_tracks': queue_items[:5]
        }