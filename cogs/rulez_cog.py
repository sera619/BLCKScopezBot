import disnake
from disnake.ext import commands
from core.config import ROLE_RULE_ID, RULES_CHANNEL_ID
from views.rollbutton_view import RuleButtonView


class RulezCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    async def post_rules(self):
        guild = self.bot.guilds[0]
        channel = guild.get_channel(int(RULES_CHANNEL_ID))
        role_id = int(ROLE_RULE_ID)
        
        try:
            await channel.purge(limit=100)
        except Exception as e:
            print(f"Error purge rules channel:\n{e}")
        
        embed = disnake.Embed(
        title="📜 Server Regeln",
        description=("**Willkommen!**\n"
                     "Bitte lese die Regeln und klicke unten, um die zur Kenntnisnahme zu bestätigen.\n"
                     "Damit erhältst du Zugriff auf die Kanäle des Discords."),
        color=disnake.Color.blue()
        )

        embed.add_field(
            name="§1 – Allgemeine Verhaltensregeln",
            value=(
                "1️⃣ Freundlicher und respektvoller Umgang mit allen Spielern\n\n"
                "2️⃣ Nicknames/Profilbilder dürfen keine Beleidigungen, Provokationen, pornografische oder rassistische Inhalte enthalten\n\n"
                "3️⃣ Hack-/DDoS-Angriffe gegen den Server werden nicht geduldet (HackBack möglich)\n\n"
                "4️⃣ Private Daten dürfen ohne Einverständnis nicht geteilt werden\n\n"
                "5️⃣ Spam ist verboten\n\n"
                "6️⃣ Systemfehler/-bugs dürfen nicht ausgenutzt werden, bitte melden\n\n"
                "7️⃣ Unwissenheit schützt nicht vor Strafe\n\n"
                "8️⃣ Kick/Bann ist immer begründet, dient zur Reflektion\n\n"
                "9️⃣ Keine Form von Diskriminierung wie Rassismus oder Sexismus"
            ),
            inline=False
        )

        embed.add_field(
            name="§2 - Verbotene Inhalte",
            value=(
            "1️⃣ Erotische oder pornografische Inhalte/Links\n\n"
            "2️⃣ Rassistische oder belästigende Inhalte\n\n"
            "3️⃣ Beleidigungen oder Hetze gegen Personen oder Projekte"
            ),
            inline=False
        )
        embed.set_footer(text="Das BLCKScopez Support-Team bedankt sich!\nViel Spaß!")
        view = RuleButtonView(role_id=role_id)
        await channel.send(embed=embed, view=view)
        
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        await self.post_rules()


def setup(bot: commands.Bot):
    bot.add_cog(RulezCog(bot))