from disnake.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
     
    @commands.command(name="reload")
    @commands.has_permissions(administrator=True)
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, cog: str):
        try:
            self.bot.reload_extension(f"cogs.{cog}")
            await ctx.send(f"Start hot-reload.\nHot-Reloaded **{cog}**", delete_after=7)
        except Exception as e:
            await ctx.send(f"Error hot-reloading {cog}:\n```{e}```", delete_after=7)
            
    @commands.command(name="reloadall")
    @commands.has_permissions(administrator=True)
    @commands.is_owner()
    async def reload_all(self, ctx: commands.Context):
        reloaded = []
        for ext in list(self.bot.extensions):
            try:
                self.bot.reload_extension(ext)
                reloaded.append(ext)
            except Exception as e:
                await ctx.send(f"Error reload extension `{ext}`:\n```{e}```", delete_after=7)
        await ctx.send(f"Hot-Reloaded:\n"+"\n".join(reloaded), delete_after=7)

    # errohandling
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("Du hast leider nich die nötigen Recht um diesen Befehl auszuführen!")
        elif isinstance(error, commands.CommandNotFound):
            pass
        else:
            await ctx.send(f"Ein Fehler ist aufgetreten:\n```{error}```")
    
def setup(bot: commands.Bot):
    bot.add_cog(Admin(bot))
                