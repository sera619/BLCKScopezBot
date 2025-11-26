import disnake
from disnake.ext import commands
from core.config import BOT_ICON_URL, BOT_VERSION, DISCORD_SERVER_ID
import utils

class BotinfoCommands(commands.Cog):    
    def __init__(self, bot):
        self.bot = bot
        self.bot_icon_url = BOT_ICON_URL

    @commands.slash_command(name="botinfo", 
                            description="Zeigt die Informationen über den Bot.",
                            default_member_permissions=disnake.Permissions(administrator=True),
                            guild_ids=[int(DISCORD_SERVER_ID)])
    async def botinfo(self, ctx):
        file_path = utils.resource_path("data/bot_icon.png") 
        file = disnake.File(file_path, filename="bot_icon.png")
        embed = disnake.Embed(
            title="BLCKScopez Bot - Info",
            description=(
                f"Der Bot ist online und bereit für Action.\n"
                f"Version: {BOT_VERSION}\n"
                "_Um alle Botbefehle zu sehen gebe **/hilfe** ein._"
            ),
            color=disnake.Color.dark_gray()
        )
        embed.set_thumbnail(url=BOT_ICON_URL)
        embed.set_footer(text="No system is safe – expect us.\nThis bot is under development\n\n© S3R43o3 2025")
        await ctx.send(embed=embed, file=file)


def setup(bot: commands.Bot):
    bot.add_cog(BotinfoCommands(bot))