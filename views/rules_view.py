import disnake
from disnake.ext import commands

class RulesView(disnake.ui.View):
    def __init__(self, role_id: int):
        super().__init__(timeout=None)
        self.role_id = role_id

    # Main overview button
    @disnake.ui.button(label="📘 Übersicht", style=disnake.ButtonStyle.gray, row=0)
    async def overview(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):

        embed = disnake.Embed(
            title="📘 Server Regeln – Übersicht",
            color=disnake.Color.green(),
            description=(
                "Wähle ein Kapitel aus dem Menü unten, um die Regeln anzusehen.\n\n"
                "✔ §1 Allgemeine Verhaltensregeln\n"
                "✔ §2 Verbotene Inhalte\n"
            )
        )

        await interaction.response.edit_message(embed=embed, view=self)
        
        
    # SECTION 1 – Allgemeine Verhaltensregeln
    @disnake.ui.button(label="§1 Allgemeine Regeln", style=disnake.ButtonStyle.gray, row=1)
    async def section1(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):

        # Create updated embed
        embed = disnake.Embed(
            title="📘 §1 – Allgemeine Verhaltensregeln",
            color=disnake.Color.blue(),
            description=(
                "### 1️⃣ Freundlicher und respektvoller Umgang mit allen Spielern\n"
                "### 2️⃣ Nicknames/Profile dürfen keine Beleidigungen, Provokationen, pornografische oder rassistische Inhalte enthalten\n"
                "### 3️⃣ Hack-/DDoS-Angriffe gegen den Server werden nicht geduldet (HackBack möglich)\n"
                "### 4️⃣ Private Daten dürfen ohne Einverständnis nicht geteilt werden\n"
                "### 5️⃣ Spam ist verboten\n"
                "### 6️⃣ Systemfehler/Bugs dürfen nicht ausgenutzt werden, bitte melden\n"
                "### 7️⃣ Unwissenheit schützt nicht vor Strafe\n"
                "### 8️⃣ Kick/Bann ist immer begründet, dient zur Reflexion\n"
                "### 9️⃣ Keine Form von Diskriminierung wie Rassismus oder Sexismus\n"
            )
        )

        # Update the message
        await interaction.response.edit_message(embed=embed, view=self)

    # SECTION 2 – Verbotene Inhalte
    @disnake.ui.button(label="§2 Verbotene Inhalte", style=disnake.ButtonStyle.gray, row=1)
    async def section2(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):

        embed = disnake.Embed(
            title="🚫 §2 – Verbotene Inhalte",
            color=disnake.Color.red(),
            description=(
                "### 🔞 1️⃣ Erotische oder pornografische Inhalte/Links\n"
                "### 🛑 2️⃣ Rassistische oder belästigende Inhalte\n"
                "### ⚠️ 3️⃣ Beleidigungen oder Hetze gegen Personen oder Projekte\n"
            )
        )

        await interaction.response.edit_message(embed=embed, view=self)

    # Confirm button (Regeln gelesen)
    @disnake.ui.button(label="✔ Regeln gelesen", style=disnake.ButtonStyle.success, row=3)
    async def confirm(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        guild = interaction.guild
        member = interaction.user
        role = guild.get_role(self.role_id)
        
        if role in member.roles:
            await interaction.response.send_message("Du hast die Rolle bereits!", ephemeral=True, delete_after=7)
        else:
            await member.add_roles(role)
            await interaction.response.send_message(f"Alles klar, du hast die Regeln bestätigt! ✔\nRolle **{role.name}** wurde vergeben!",
                ephemeral=True, delete_after=10)
