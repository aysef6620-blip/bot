# 🎵 YouTube Live Chat Music Request Bot

Canlı YouTube yayınında izleyicilerin `!sr` komutuyla müzik isteyebilmesi sağlayan bot.

## ✨ Özellikler

- 🎵 Live Chat'ten müzik istekleri al
- 🔍 YouTube'da müzik ara
- ⬇️ Otomatik indirme (MP3)
- ▶️ Müzik çalma kuyruğu
- ⏭️ Şarkı atla / Duraklat / Devam et
- 📊 Kuyruk göster
- 🛡️ Rate limiting (spam koruması)

## 📋 Komutlar

| Komut | Açıklama | Örnek |
|-------|----------|--------|
| `!sr <şarkı>` | Müzik iste | `!sr Dua Lipa Levitating` |
| `!queue` veya `!q` | Kuyruk göster | `!q` |
| `!skip` | Şarkı atla | `!skip` |
| `!pause` | Duraklat | `!pause` |
| `!resume` | Devam et | `!resume` |
| `!help` | Yardım | `!help` |

## 🚀 Kurulum

### 1. Gereksinimler

- Python 3.8+
- FFmpeg (MP3 indirme için)

### 2. FFmpeg Yükleme

**Windows:**
```bash
# Chocolatey kullanarak
choco install ffmpeg
```

**macOS:**
```bash
# Homebrew kullanarak
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg
```

### 3. Python Paketlerini Yükle

```bash
pip install -r requirements.txt
```

## 🔑 YouTube API Kurulumu

### 1. Google Cloud Console'da Proje Oluştur
1. https://console.cloud.google.com/ gir
2. Yeni proje oluştur
3. "YouTube Data API v3" etkinleştir

### 2. API Key Oluştur
1. "API ve Hizmetler" → "Kimlik Bilgileri" git
2. "Kimlik bilgisi oluştur" → "API Anahtarı" seç
3. Oluşturulan API key'i kopyala

### 3. Live Chat ID Bul

**Yayın başladıktan sonra:**

```python
# Python'da bunu çalıştır:
from youtube_api import YouTubeAPI

api = YouTubeAPI()
# Canlı yayınının video ID'si ile:
# https://www.youtube.com/watch?v={VIDEO_ID}
```

Veya YouTube Studio'dan:
1. YouTube Studio'ya gir
2. Canlı yayın bilgisini aç
3. "Paylaş" → URL'den video ID'ni al
4. API üzerinden Live Chat ID'yi bul

## ⚙️ Konfigürasyon

`.env` dosyası oluştur:

```env
YOUTUBE_API_KEY=your_api_key_here
LIVE_CHAT_ID=your_live_chat_id_here
BOT_PREFIX=!
COMMAND=sr
```

## ▶️ Çalıştırma

```bash
python bot.py
```

Bot çıktısı:
```
🤖 Bot başlatılıyor...
✅ Bot hazır!
📝 Komut: !sr
💬 Live Chat ID: xxxxx
👀 Chat izlenmeye başlandı...
```

## 📁 Dosya Yapısı

```
bot/
├── bot.py                 # Ana bot dosyası
├── config.py              # Konfigürasyon
├── youtube_api.py         # YouTube API işlemleri
├── music_player.py        # Müzik çalma
├── downloader.py          # Video indirme
├── requirements.txt       # Python paketleri
├── .env                   # API anahtarları (.gitignore'da)
└── downloads/             # İndirilen müzikler
```

## 🛡️ Özellikler

### Rate Limiting
- Kullanıcı başına maksimum 3 istek
- Bot spam'ı otomatik olarak engeller

### Disk Tasarrufu
- Eski dosyalar otomatik silinir
- Maksimum 100 dosya tutulur

### Error Handling
- Hata yönetimi ve otomatik kurtarma
- Bağlantı koptuğunda yeniden bağlanma

## ⚠️ Sınırlamalar

- YouTube API'ın rate limitleri vardır
- FFmpeg gereklidir
- İnternet bağlantısı gereklidir

## 🐛 Sorun Giderme

### "API key invalid" hatası
- API key'in doğru olup olmadığını kontrol et
- YouTube Data API'ın etkinleştirildiğini kontrol et

### "Live Chat ID not found" hatası
- Yayının canlı olduğundan emin ol
- Live Chat ID'yi düzgün kopyaladığından emin ol

### Müzik çalmıyor
- FFmpeg'in yüklü olduğunu kontrol et
- İndirme klasörünün yazılabilir olduğunu kontrol et

## 📝 Lisans

MIT

## 👤 Yazar

Oluşturan: aysef6620-blip

---

**Sorular veya sorunlar?** Issues açabilirsin!
