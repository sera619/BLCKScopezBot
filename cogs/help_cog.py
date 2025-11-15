import disnake
from disnake.ext import commands
from core.config import BOT_ICON_URL, DISCORD_SERVER_ID

class HelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name="hilfe", 
                            description="Zeigt das Hilfemenü des Bots.",
                            guild_ids=[int(DISCORD_SERVER_ID)])
    async def show_help(self, ctx):
        f = disnake.File("data/bot_icon.png", filename="bot_icon.png")
        embed = disnake.Embed(
            title="BLCKScopez Bot - Hilfe",
            description=(
                "Nachfolgend sind alle Befehle aufgelistet:\n\n"
                "**/botinfo** - zeigt Informationen über den Bot\n"
                "**/twitch** - zeigt den Link zum Twitchstream.\n"
                "**/stream_zeiten** - zeigt die aktuellen Streamzeiten an\n"
                "**/hilfe** - zeigt die Hilfe an\n\n"
                "___Admin Commands___\n\n"
                "**/clear_messages** - Löscht 1000 Nachrichten aus einem Channel\n"
                "**/create_streamembed** - Erstellt im News-Channel eine neue Infotafel für den Stream\n"
                "**/create_clip** - Erstellt im clip channel eine neue infotafel.\n"
            ),
            color= disnake.Color.dark_red()
        )
        embed.set_footer(text="Weitere Funktionen folgen bald.\n© S3R43o3 2025")
        embed.set_thumbnail(url=BOT_ICON_URL)
        await ctx.send(embed=embed, file=f)

def setup(bot: commands.Bot):
    bot.add_cog(HelpCommands(bot))