import disnake
from disnake.ext import commands
from core.config import BOT_ICON_URL, TWITCH_ICON_URL, TWITCH_URL, DISCORD_SERVER_ID

class TwitchCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.slash_command(name="twitch", 
                            description="Zeigt den Link zum Twitch-Stream.",
                            guild_ids=[int(DISCORD_SERVER_ID)])
    async def send_twitch(self, ctx):
        f = disnake.File("bot_icon.png", filename="bot_icon.png")
        embed = disnake.Embed(
            title="BLCKScopez Bot - Twitch-Kanal",
            url=TWITCH_URL,
            description="Klick oben auf den Titel, um direkt zum Stream zu kommen!",
            color=disnake.Color.purple()
        )
        embed.set_thumbnail(url=BOT_ICON_URL)
        embed.set_image(url=TWITCH_ICON_URL)
        await ctx.send(embed=embed, file=f)
        
def setup(bot: commands.Bot):
    bot.add_cog(TwitchCommands(bot))