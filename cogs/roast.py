import disnake
from disnake.ext import commands
from core.config import OPENAI_API_KEY, DISCORD_SERVER_ID
from openai import AsyncOpenAI


client = AsyncOpenAI(api_key=OPENAI_API_KEY)

class RoastAI(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @commands.slash_command(description="Roast einen User mit KI 🤖🔥", guild_ids=[int(DISCORD_SERVER_ID)])
    async def roast(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User):
        await inter.response.defer()

        prompt = (
            f"Give me a short, funny, witty roast for the user '{user.name}'. "
            "Keep it under 25 words. Dark humor is allowed. "
            "Do NOT use slurs, politics, protected groups, or targeting disabilities. "
            "Make it playful but spicy."
        )

        try:
            response = await client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=60,
                temperature=0.9
            )

            roast_text = response.choices[0].message.content.strip()

            embed = disnake.Embed(
                title="🔥 KI Roast",
                description=roast_text,
                color=disnake.Color.red()
            )
            embed.set_footer(text=f"Requested by {inter.author.name}")

            await inter.followup.send(embed=embed)

        except Exception as e:
            await inter.followup.send(f"Fehler beim Roast: {e}")

def setup(bot):
    bot.add_cog(RoastAI(bot))