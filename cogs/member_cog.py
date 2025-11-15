import disnake
from disnake.ext import commands


class MemberEvent(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        print(f"Member {member.name} joined discord.")
        sys_channel = member.guild.system_channel 
        if sys_channel:
            await sys_channel.send(f"Willkommen im Irrenhaus, {member.display_name}! :wave:\n")


def setup(bot: commands.Bot):
    bot.add_cog(MemberEvent(bot))
        