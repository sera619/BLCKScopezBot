import disnake
import logging
from disnake.ext import commands
from core.config import BOT_VERSION, BOT_CHANNEL_ID, TWITCH_ICON_URL, BOT_ICON_URL, TWITCH_URL, NEWS_CHANNEL_ID
from core.logger import logger

class BLCKScopezBot(commands.Bot):
    def __init__(self):
        intents = disnake.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.messages = True
        intents.presences = True

        super().__init__(
            command_prefix="!",
            intents= intents
        )        
        
        self.bot_channel_id = BOT_CHANNEL_ID
        self.twitch_icon_url = TWITCH_ICON_URL
        self.bot_icon_url = BOT_ICON_URL
        self.twitch_url = TWITCH_URL
        self.send_starup_message = False
      
    async def on_ready(self):
        # print(f"logged in as: {self.user} | User ID: {self.user.id}")
        await self.get_channels()
        await self._sync_application_commands()
        activity = disnake.Activity(
            type=disnake.ActivityType.competing,
            name="/hilfe für Infos."
        )
        
        await self.change_presence(status=disnake.Status.dnd, activity=activity)
        print(f"Bot {self.user} is now online!")
        logger.info(f"Bot {self.user} is now online!")
        
    async def on_message(self, message):
        # ignore messages from bot itself
        if message.author.id == self.user.id:
            return 
        # print(f"Message from: {message.author}:\n{message.content}")
        logger.debug(f"Message from {message.author}: {message.content}")
        await self.process_commands(message)  # WICHTIG, sonst funktionieren Commands nicht!
        
    async def on_disconnect(self):
        print(f"Bot {self.user} lost conection or get stopped!")
        logger.warning(f"Bot {self.user} lost connection or was stopped!")
        
    async def close(self):
        print("Bot get shutting down...")
        await super().close()
        print("Bot now offline!")        
        
    async def start_up_message(self, channel_to_send):
        file = disnake.File("data/bot_icon.png", filename="bot_icon.png")
        embed = disnake.Embed(
            title="BLCKScopez Bot successfully started!",
            description=(
                    "Der Bot ist jetzt online und bereit für Action.\n"
                    "Alle Systeme laufen stabil.\n\n"
                    "**Status:** OK\n"
                    f"**Version:** {BOT_VERSION}\n\n"
                    "_Um alle Botbefehle zu sehen gebe **/hilfe** ein._"),
            color=disnake.Color.dark_gray()
        )
        embed.set_thumbnail(url=BOT_ICON_URL)
        embed.set_footer(text="No system is safe – expect us.\nThis bot is under development\n\n© S3R43o3 2025")
        logger.info(f"Startup message sent to channel ID {channel_to_send.id}")
        await channel_to_send.send(embed=embed, file = file,)

    async def get_channels(self):
        # for guild in self.guilds:
        #     print(f"Guild: {guild.name} | ID {guild.id}")
        #     for channel in guild.channels:
        #         print(f"- {channel.name} ID: {channel.id}")
        
        # try to find the "bot-commands" channel
        startup_channel =  None
        for guild in self.guilds:
            for channel in guild.text_channels:
                if channel.id == self.bot_channel_id:
                    startup_channel = channel
                    break
            if startup_channel:
                break
        
        
        if startup_channel:
            if self.send_starup_message:
                await self.start_up_message(startup_channel)
            else:
                return
        else:
            print("No 'bot-commands' channel found")
            logger.warning("No 'bot-commands' channel found")
        
        