import disnake
from disnake.ext import commands
from core.config import BOT_ICON_URL, DISCORD_SERVER_ID, NEWS_CHANNEL_ID, TWITCH_URL
import utils

class StreamEmbedCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot    
    
    # Testcommand: /create_streamembed title:Test description:test date:11.12.2025 start_time:13:00
    @commands.slash_command(name="create_streamembed", 
                            description="Erstellt eine Nachricht für den nächsten Stream. (Admin)",
                            default_member_permissions=disnake.Permissions(administrator=True),
                            guild_ids=[int(DISCORD_SERVER_ID)])
    async def create_stream_embed(self,
                                  inter: disnake.ApplicationCommandInteraction, 
                                  title: str, 
                                  description: str,
                                  date: str, 
                                  start_time: str):
        file_path = utils.resource_path("data/bot_icon.png") 
        f = disnake.File(f"{file_path}", filename="bot_icon.png")
        embed = disnake.Embed(
            title=f"{title}",
            description=(f"***{description}***\n\n"
                         f"**Datum:** {date}\n"   
                         f"**Startzeit:** {start_time} Uhr\n"
                         f"**Link:** {TWITCH_URL}\n\n"
                         "**Wir freuen uns euch dort begrüßen zu dürfen!**"),
            colour=disnake.Colour.dark_gold()
        )
        embed.set_thumbnail(url=BOT_ICON_URL)
        
        # get news hannel 
        news_channel = self.bot.get_channel(NEWS_CHANNEL_ID)
        if news_channel is None:
            await inter.response.send_message("Fehler: News-Channel nicht gefunden!", ephemeral=True,delete_after=7)
            return

        await news_channel.send(embed=embed, file=f)
        await inter.response.send_message(f"Embed erfolgreich im News-Channel gepostet!", ephemeral=True, delete_after=7)
        
def setup(bot: commands.Bot):
    bot.add_cog(StreamEmbedCog(bot))