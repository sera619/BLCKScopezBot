import disnake
from disnake.ext import commands
from core.config import BOT_ICON_URL, DISCORD_SERVER_ID

class SheduleCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="stream_zeiten", 
                            description="Zeigt die aktuellen Streamingzeiten an.",
                            guild_ids=[int(DISCORD_SERVER_ID)])
    async def zeiten(self, ctx):
        file = disnake.File("data/bot_icon.png", filename="bot_icon.png")
        embed = disnake.Embed(
            title="BLCKScopez Bot - Streamzeiten",
            description=("Aktuell gibt es noch keine festen Streamzeiten.\n\n"
                         f"**Montag:**       --:-- Uhr\n"
                         f"**Dienstag:**     --:-- Uhr\n"
                         f"**Mittwoch:**     --:-- Uhr\n"
                         f"**Donnerstag:**   --:-- Uhr\n"
                         f"**Freitag:**      --:-- Uhr\n"
                         f"**Samstag:**      --:-- Uhr\n"
                         f"**Sonntag:**      --:-- Uhr\n"
                         ),
            color=disnake.Color.dark_red()
        )
        embed.set_thumbnail(url=BOT_ICON_URL)
        await ctx.send(embed=embed, file=file)


def setup(bot: commands.Bot):
    bot.add_cog(SheduleCommands(bot))