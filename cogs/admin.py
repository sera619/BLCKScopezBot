from disnake.ext import commands

class Adim(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    
    # TODO: Errorhandling without adminrights
     
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

    
def setup(bot: commands.Bot):
    bot.add_cog(Adim(bot))
                