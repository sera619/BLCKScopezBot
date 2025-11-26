import disnake
from core.logger import logger

class RuleButtonView(disnake.ui.View):
    def __init__(self, role_id: int):
        super().__init__(timeout=None)
        self.role_id = role_id
    
    @disnake.ui.button(label="📜 Regeln gelesen", style=disnake.ButtonStyle.green, custom_id="rulez_button")
    async def role_button(self, button: disnake.ui.button, interaction: disnake.MessageInteraction):
        guild = interaction.guild
        member = interaction.user
        role = guild.get_role(self.role_id)

        if role in member.roles:
            await interaction.response.send_message("Du hast die Rolle bereits!", ephemeral=True, delete_after=7)
        else:
            logger.info(f"User:{member} from guild: {guild} get the role: {role}!")
            await member.add_roles(role)
            await interaction.response.send_message(f"Rolle **{role.name}** vergeben!", ephemeral=True, delete_after=7)
