import os
from dotenv import load_dotenv

load_dotenv()

# YouTube API Configuration
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY', '')
LIVE_CHAT_ID = os.getenv('LIVE_CHAT_ID', '')

# Bot Configuration
BOT_PREFIX = os.getenv('BOT_PREFIX', '!')
COMMAND = os.getenv('COMMAND', 'sr')
FULL_COMMAND = f"{BOT_PREFIX}{COMMAND}"

# Music Player Configuration
MUSIC_FOLDER = './downloads'
MAX_QUEUE_SIZE = 50
SKIP_VOTES_NEEDED = 3

# Check if music folder exists
if not os.path.exists(MUSIC_FOLDER):
    os.makedirs(MUSIC_FOLDER)