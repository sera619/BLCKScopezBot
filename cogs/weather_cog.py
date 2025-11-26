import disnake
import aiohttp 
from disnake.ext import commands
from core.config import DISCORD_SERVER_ID, BOT_ICON_URL
from datetime import datetime

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

class WeatherCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_coords(self, city: str):
        """Convert ZIP code to lat/lon with proper error handling."""
        params = {
            "name": city,
            "count": 1,
            "language": "de",
            "format": "json"
        }

        async with aiohttp.ClientSession() as s:
            async with s.get(GEOCODE_URL, params=params) as r:
                if r.status != 200:
                    print("GEOCODE API ERROR:", r.status)
                    return None

                data = await r.json()
                print("GEOCODE RESPONSE:", data)

                if "results" not in data or len(data["results"]) == 0:
                    return None

                result = data["results"][0]
                return {"lat": result["latitude"], "lon": result["longitude"]}

    async def get_weather(self, lat: float, lon: float):
        """Fetch current weather safely."""
        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": "true",  # MUST be string
            "timezone": "Europe/Berlin"
        }

        async with aiohttp.ClientSession() as s:
            async with s.get(WEATHER_URL, params=params) as r:
                if r.status != 200:
                    print("WEATHER API ERROR:", r.status)
                    return None

                data = await r.json()
                print("WEATHER RESPONSE:", data)

                if "current_weather" not in data:
                    return None

                return data["current_weather"]

    @commands.slash_command(name="wetter", description="Zeigt das aktuelle Wetter für eine Postleitzahl an.", guild_ids=[int(DISCORD_SERVER_ID)])
    async def wetter(self, inter: disnake.ApplicationCommandInteraction, city: str):
        await inter.response.defer()

        coords = await self.get_coords(city)
        if not coords:
            return await inter.edit_original_response("❌ Konnte die Koordinaten nicht abrufen. Ist der Ortsname korrekt?")

        weather = await self.get_weather(coords["lat"], coords["lon"])
        if not weather:
            return await inter.edit_original_response("❌ Konnte das Wetter nicht abrufen.")

        temp = weather["temperature"]
        wind = weather["windspeed"]
        direction = weather["winddirection"]
        raw_time = weather["time"]
        parsed = datetime.fromisoformat(raw_time)
        time = parsed.strftime("%d.%m.%Y %H:%M Uhr")
        
        f = disnake.File("data/bot_icon.png", filename="bot_icon.png")

        embed = disnake.Embed(
            title=f"Wetter in {city}",
            description=f"Stand: **{time}**",
            color=0x00aaff
        )
        embed.add_field(name="🌡️ Temperatur", value=f"{temp} °C", inline=False)
        embed.add_field(name="💨 Windgeschwindigkeit", value=f"{wind} km/h", inline=False)
        embed.add_field(name="🧭 Windrichtung", value=f"{direction}°", inline=False)
        embed.set_thumbnail(url=BOT_ICON_URL)
        await inter.edit_original_response(embed=embed, file=f)


def setup(bot: commands.Bot):
    bot.add_cog(WeatherCog(bot))