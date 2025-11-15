import disnake
from disnake.ext import commands
from core.config import  BOT_CHANNEL_ID, ROLE_RULE_ID
from views.rules_view import RulesView


class TestrulesCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    async def post_testrules(self):
        guild = self.bot.guilds[0]
        channel = guild.get_channel(BOT_CHANNEL_ID)
        role_id = int(ROLE_RULE_ID)
        embed = disnake.Embed(
            title="📘 Server Regeln – Übersicht",
            color=disnake.Color.blurple(),
            description=(
                "Wähle ein Kapitel aus dem Menü unten, um die Regeln anzusehen.\n\n"
                "✔ §1 Allgemeine Verhaltensregeln\n"
                "✔ §2 Verbotene Inhalte\n"
            )
        )
        await channel.send(embed=embed, view=RulesView(role_id=role_id))
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        await self.post_testrules()


def setup(bot: commands.Bot):
    bot.add_cog(TestrulesCog(bot))