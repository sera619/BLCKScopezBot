import disnake
from disnake.ext import commands
from core.config import BOT_ICON_URL, DISCORD_SERVER_ID, VOICE_CREATE_CHANNEL_ID
from core.logger import logger
import utils


class HelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name="hilfe", 
                            description="Zeigt das Hilfemenü des Bots.",
                            guild_ids=[int(DISCORD_SERVER_ID)])
    async def show_help(self, ctx):
        voicecreate_channel = ctx.guild.get_channel(VOICE_CREATE_CHANNEL_ID)
        voicecreate_channel_link = f"<#{voicecreate_channel.id}>"
        file_path = utils.resource_path("data/bot_icon.png") 
        f = disnake.File(f"{file_path}", filename="bot_icon.png")
        embed = disnake.Embed(
            title="BLCKScopez Bot - Hilfe",
            description=(
                "Nachfolgend sind alle Befehle aufgelistet:\n\n"
                "**/botinfo** - zeigt Informationen über den Bot\n"
                "**/twitch** - zeigt den Link zum Twitchstream.\n"
                "**/stream_zeiten** - zeigt die aktuellen Streamzeiten an\n"
                "**/wetter <Ortsname>** - zeigt das aktuelle Wetter für den Ortan\n"
                "**/hangman start** - Starten ein Hangmanspiel im Channel.\n"
                "**/hangman guess <Buchstabe>** - Rät einen Buchstaben im Hangmanspiel.\n"
                "**/hangman stop** - Beendet das aktuelle Hangmanspiel im Channel.\n"
                "**/hangman leaderboard** - Zeige die Serverweite Hangman-Rangliste.\n"
                "**/hilfe** - zeigt die Hilfe an\n\n"
                "___Admin Commands___\n\n"
                "**/clear_messages** - Löscht 1000 Nachrichten aus einem Channel\n"
                "**/create_streamembed** - Erstellt im News-Channel eine neue Infotafel für den Stream\n"
                "**/create_clip** - Erstellt im clip channel eine neue infotafel.\n\n"
                f"Weiterhin ist es möglich über den Channel {voicecreate_channel_link} einen temporären Voice-Channel für maximal 2 User zu erstellen.\n\n"
                "___Development Commands___\n\n"
                "**WICHTIG! DIESE BEFEHLE DÜRFEN AUCH NICHT VON ADMINS BENUTZT WERDEN!\nDIESE SIND ALLEIN FÜR S3R43o3!**\n\n"
                "**!reloadall** - Hot-Reload für ALLE Extensions.\n"
                "**!reload <ext. name>** - Hot-Reload für einzelne Extensions.\n"
                "**!postwelcome** - Geht keinen was an.\n"
                "**!devpanel** - Zeigt den Cog-Manager"
            ),
            color= disnake.Color.dark_red()
        )
        embed.set_footer(text="Weitere Funktionen folgen bald.\n© S3R43o3 2025")
        embed.set_thumbnail(url=BOT_ICON_URL)
        logger.info(f"User {ctx.user} used '/hilfe' command!")
        await ctx.send(embed=embed, file=f)

def setup(bot: commands.Bot):
    bot.add_cog(HelpCommands(bot))