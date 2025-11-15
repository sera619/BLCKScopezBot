import asyncio, disnake, sys, os
from disnake.ext import commands

from core.config import DISCORD_TOKEN
from core.botcore import BLCKScopezBot


bot = BLCKScopezBot()

def load_cogs(bot: commands.Bot):
    #print("Initialize Cogs...\n")
    counter = 0
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and not filename.startswith("_"):
            cog = f"cogs.{filename[:-3]}"
            # if cog =="cogs.rulez_cog":
            #     continue
            counter += 1
            #print(f"{counter}) Cog successfully loaded: {cog}")
            bot.load_extension(cog)
    print(f"\n{counter}s Cogs successfully loaded!")

def setup_bot():
    load_cogs(bot)

def main():
    setup_bot()
    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occured:\n{e}")
    finally:
        sys.exit()
