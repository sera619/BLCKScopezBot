import disnake
from disnake.ext import commands
from core.config import SERA_ID

class VoiceEvent(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot        
    
    # Voice listener
    @commands.Cog.listener()
    async def on_voice_state_update(self, 
                                    member: disnake.Member,
                                    before: disnake.VoiceState,
                                    after: disnake.VoiceState):
        
        # user joins channel
        if before.channel is None and after.channel is not None:
            vc = after.channel
            if vc: 
                await vc.send(f" **{member.display_name}** joined!")
                if member.id == int(SERA_ID):
                    deleted = await vc.purge(limit=100)
                    await vc.send(f"✅ Gelöscht {len(deleted)} Nachrichten.", delete_after=5)
            return
        
        # user leaves channel
        if before.channel is not None and after.channel is None:
            print(f"{member} left {before.channel.name}!")
            return
        
        # user changes voicechannel
        if before.channel != after.channel:
            print(f"{member} switched from {before.channel.name} to {after.channel.name}!")
            return


def setup(bot: commands.Bot):
    bot.add_cog(VoiceEvent(bot))