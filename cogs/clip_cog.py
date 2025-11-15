import disnake
from disnake.ext import commands
from core.config import DISCORD_SERVER_ID, CLIP_CHANNEL_ID, BOT_ICON_URL


class ClipCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot   
    
    # testcommand: /create_clip title:Neuer Clip  description:Geiler neuer Clip  clip_url:https://www.twitch.tv/blckscopez/clip/VastSpotlessCatHeyGuys-DETFwXlqyhHVFs58
    @commands.slash_command(name="create_clip",
                            description="Erstellt einen neuen Banner für einen Twitch-Clip. (Admin)",
                            default_member_permissions=disnake.Permissions(administrator=True),
                            guild_ids=[int(DISCORD_SERVER_ID)])
    async def create_clip_embed(self,
                                inter: disnake.ApplicationCommandInteraction, 
                                title: str,
                                description: str,
                                clip_url: str):
        f = disnake.File("data/bot_icon.png", filename="bot_icon.png")
        embed = disnake.Embed(
            title=title,
            description=description,
            color=disnake.Color.dark_gold()
        )
        embed.set_thumbnail(file=f)
        
        # get clip channel
        clip_channel = self.bot.get_channel(CLIP_CHANNEL_ID)
        if clip_channel is None:
            await inter.response.send_message("Fehler: Clip-Channel nicht gefunden!", ephemeral=True,delete_after=7)
            return
        await clip_channel.send(embed=embed)
        await clip_channel.send(clip_url)
        await inter.response.send_message(f"Clip-Embed erfolgreich im Clip-Channel gepostet!", ephemeral=True, delete_after=7)


def setup(bot: commands.Bot):
    bot.add_cog(ClipCog(bot))