from dotenv import load_dotenv
import os

load_dotenv()
BOT_VERSION = "1.4.8"

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TWITCH_ICON_URL = "https://static.twitchcdn.net/assets/favicon-32-e29e246c157142c94346.png"
BOT_ICON_URL = 'attachment://bot_icon.png'
TWITCH_URL = "https://www.twitch.tv/blckscopez"
DISCORD_SERVER_ID = os.getenv("DISCORD_SERVER_ID")
BOT_CHANNEL_ID = int(os.getenv("BOT_CHANNEL_ID"))
NEWS_CHANNEL_ID = int(os.getenv("NEWS_CHANNEL_ID"))
CLIP_CHANNEL_ID = int(os.getenv("CLIP_CHANNEL_ID"))
LOUNCH_CHANNEL_ID = int(os.getenv("LOUNCH_CHANNEL_ID"))
SERA_ID = os.getenv("SERA_ID")
RULES_CHANNEL_ID = os.getenv("RULES_CHANNEL_ID")