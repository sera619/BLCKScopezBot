import disnake
from disnake.ext import commands
from core.config import DISCORD_SERVER_ID

class PurgeCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    # purge all messages in channel
    @commands.slash_command(name="clear_messages",
                            description="Löscht die letzten 1000 Nachrichten aus dem Channel. (Admin)",
                            default_member_permissions=disnake.Permissions(administrator=True),
                            guild_ids=[int(DISCORD_SERVER_ID)])
    async def clear_messages(self, ctx, limit: int = None):
        if limit is None:
            limit = 1000
        deleted = await ctx.channel.purge(limit=limit)
        await ctx.send(f"✅ Gelöscht {len(deleted)} Nachrichten.", delete_after=5)


def setup(bot: commands.Bot):
    bot.add_cog(PurgeCog(bot))