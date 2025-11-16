import disnake
from disnake.ext import commands
from views.dev_cogmanager_view import CogManagerView

class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.welcome_msg_filepath = "./data/welcome_message.md"
     
    @commands.command(name="reload")
    @commands.has_permissions(administrator=True)
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, cog: str):
        try:
            await ctx.message.delete()
            await ctx.send(f"Start hot-reloading Extension: **{cog}**...", delete_after=7)
            self.bot.reload_extension(f"cogs.{cog}")
        except Exception as e:
            await ctx.send(f"Error hot-reloading {cog}:\n```{e}```", delete_after=7)
    
            
    @commands.command(name="reloadall")
    @commands.has_permissions(administrator=True)
    @commands.is_owner()
    async def reload_all(self, ctx: commands.Context):
        reloaded = []
        await ctx.message.delete()
        await ctx.send(f"Start hot-reloading ALL extensions...", delete_after=4)
        for ext in list(self.bot.extensions):
            try:
                self.bot.reload_extension(ext)
                reloaded.append(ext)
            except Exception as e:
                await ctx.send(f"Error reload extension `{ext}`:\n```{e}```", delete_after=7)
        await ctx.send(f"Successfully hot-reloaded:\n"+"\n".join(reloaded), delete_after=7)
        
        
    # devpanel
    @commands.command(name="devpanel")
    @commands.has_permissions(administrator=True)
    @commands.is_owner()
    async def devpanel(self, ctx: commands.Context):
        embed = disnake.Embed(
            title="Developer Control Panel",
            description="Manage your bot extensions using the UI below.",
            color=0x2ECC71
        )
        embed.add_field(
            name="Available Cogs",
            value="Dynamically loaded from /cogs/",
            inline=False
        )
        
        view = CogManagerView(self.bot)
        await ctx.channel.send(embed=embed, view=view)
    
    # welcome message    
    # load welcome message
    def load_message(self) -> str:
        try:
            with open(self.welcome_msg_filepath, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Failed to load welcome message:\n```{e}```"
        
        
    # post welcome message 
    @commands.command(name="postwelcome")
    @commands.has_permissions(administrator=True)
    @commands.is_owner()
    async def post_welcome(self, ctx: commands.Context):
        await ctx.message.delete()
        msg_content = self.load_message()
        embed = disnake.Embed(
            title=" ",
            description=msg_content,
            color=0x2ECC71
        )
        await ctx.send(embed=embed)

    # error handling
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
                