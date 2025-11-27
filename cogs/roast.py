import disnake
import json
import random
from pathlib import Path
from disnake.ext import commands
from core.config import DISCORD_SERVER_ID


class RoastCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
        base = Path(__file__).parent.parent
        self.roast_file = base / "data" / "roasts.json"
        self.roasts = self.load_roasts()
        
        
    def load_roasts(self):
        """Load roasts from json file"""
        if not self.roast_file.exists():
            print("[Roast Cog] roasts.json not found!")
            return ["Die Roast-Datei konnte nicht gefunden werden!"]
        try:
            with open(self.roast_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            if isinstance(data, list) and len(data) > 0:
                return data
            else:
                print("[ROAST-Cog] roasts.json is empty or invalid.")
                return ["Die roast.json ist leer – fix das!"]
        except Exception as e:
            print(f"[Roast Cog] Error loading roast file: {e}")
            return ["Fehler beim Laden der Roast-Datei!"]
    
    @commands.slash_command(name="roast", description="Roaste einen User mit einem zufälligen Spruch.",
                            guild_ids=[int(DISCORD_SERVER_ID)])
    async def roast(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User):
        roast = random.choice(self.roasts)
        embed = disnake.Embed(
            title="🔥 Roast Maschine aktiviert",
            description=f"**{user.mention}:**\n{roast}",
            color=disnake.Color.red()
        )
        embed.set_footer(text=f"Requested by {inter.author.name}")

        await inter.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(RoastCog(bot))