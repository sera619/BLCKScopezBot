import disnake
from disnake.ext import commands
import os

class CogManagerView(disnake.ui.View):
    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=300)
        self.bot = bot

        # Build dropdown options dynamically
        options = []
        for file in os.listdir("./cogs"):
            if file.endswith(".py") and file not in ("__init__.py",):
                name = file[:-3]
                loaded = f"🟢 LOADED" if f"cogs.{name}" in bot.extensions else "🔴 OFF"
                options.append(
                    disnake.SelectOption(
                        label=name,
                        description=f"Status: {loaded}",
                        value=name
                    )
                )

        self.select = disnake.ui.Select(
            placeholder="Select a Cog to manage...",
            options=options,
            min_values=1,
            max_values=1
        )

        self.select.callback = self.select_callback
        self.add_item(self.select)

    async def select_callback(self, interaction: disnake.MessageInteraction):
        self.cog_name = self.select.values[0]
        await interaction.response.send_message(
            f"Selected **{self.cog_name}**. Choose an action below!",
            ephemeral=True
        )

    # --------------------
    # LOAD
    # --------------------
    @disnake.ui.button(label="Load", style=disnake.ButtonStyle.success)
    async def load_button(self, button, interaction):
        name = self.cog_name
        try:
            self.bot.load_extension(f"cogs.{name}")
            await interaction.response.send_message(
                f"🟢 Loaded **{name}**", ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error loading `{name}`:\n```{e}```",
                ephemeral=True
            )

    # --------------------
    # UNLOAD
    # --------------------
    @disnake.ui.button(label="Unload", style=disnake.ButtonStyle.danger)
    async def unload_button(self, button, interaction):
        name = self.cog_name
        try:
            self.bot.unload_extension(f"cogs.{name}")
            await interaction.response.send_message(
                f"🔴 Unloaded **{name}**", ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error unloading `{name}`:\n```{e}```",
                ephemeral=True
            )

    # --------------------
    # RELOAD
    # --------------------
    @disnake.ui.button(label="Reload", style=disnake.ButtonStyle.primary)
    async def reload_button(self, button, interaction):
        name = self.cog_name
        try:
            self.bot.reload_extension(f"cogs.{name}")
            await interaction.response.send_message(
                f"🔄 Reloaded **{name}**", ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error reloading `{name}`:\n```{e}```",
                ephemeral=True
            )

    # --------------------
    # RELOAD ALL
    # --------------------
    @disnake.ui.button(label="Reload All", style=disnake.ButtonStyle.primary)
    async def reload_all_button(self, button, interaction: disnake.MessageInteraction):
        reloaded = []
        for ext in list(self.bot.extensions):
            try:
                self.bot.reload_extension(ext)
                reloaded.append(ext)
            except Exception as e:
                await interaction.response.send_message(
                f"❌ Error reloading `{ext}`:\n```{e}```",
                ephemeral=True
            )
        await interaction.response.send_message(
            f"🔄 Successfully reloaded\n" +"\n".join(reloaded), 
            ephemeral=True
        )

    # --------------------
    # QUIT
    # --------------------
    @disnake.ui.button(label="Quit", style=disnake.ButtonStyle.danger, row=1)
    async def quit_panel_button(self, button, inter: disnake.MessageInteraction):
        try:
            await inter.message.delete()
        except disnake.NotFound:
            pass
        
        await inter.response.send_message(
            "Devpanel closed.", ephemeral=True
        )
    
    