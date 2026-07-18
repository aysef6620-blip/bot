import yt_dlp
import os
from config import MUSIC_FOLDER

class YouTubeDownloader:
    def __init__(self):
        self.music_folder = MUSIC_FOLDER
    
    def download_audio(self, video_url, video_title):
        """YouTube videosundan ses indir"""
        try:
            # Dosya adını temizle
            safe_title = self._sanitize_filename(video_title)
            output_path = os.path.join(self.music_folder, f"{safe_title}.mp3")
            
            # Eğer zaten indirilmişse, onu kullan
            if os.path.exists(output_path):
                print(f"📁 Önceden indirilmiş: {safe_title}")
                return output_path
            
            # yt-dlp seçenekleri
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': os.path.join(self.music_folder, safe_title),
                'quiet': False,
                'no_warnings': False,
            }
            
            print(f"⬇️ İndiriliyor: {video_title}...")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            
            print(f"✅ İndirildi: {safe_title}")
            return output_path
        
        except Exception as e:
            print(f"❌ İndirme hatası: {e}")
            return None
    
    def _sanitize_filename(self, filename):
        """Dosya adını temizle"""
        invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        for char in invalid_chars:
            filename = filename.replace(char, '')
        return filename[:100]  # Max 100 karakter
    
    def cleanup_old_files(self, max_files=100):
        """Eski dosyaları sil (disk alanı tasarrufu)"""
        try:
            files = os.listdir(self.music_folder)
            if len(files) > max_files:
                # En eski dosyaları sil
                files_with_time = [(f, os.path.getmtime(os.path.join(self.music_folder, f))) for f in files]
                files_with_time.sort(key=lambda x: x[1])
                
                for file, _ in files_with_time[:len(files) - max_files]:
                    os.remove(os.path.join(self.music_folder, file))
                print(f"🗑️ {len(files) - max_files} eski dosya silindi")
        except Exception as e:
            print(f"❌ Temizleme hatası: {e}")