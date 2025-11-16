import disnake
from disnake.ext import commands, tasks
from core.config import VOICE_CREATE_CHANNEL_ID


class TempVoice(commands.Cog):
    def __init__(self, bot: commands.Bot, channel_id: int, catergory_name: str = "Temporäre Voice"):
        self.bot = bot
        self.channel_id = channel_id
        self.category_name = catergory_name
        self.temp_channels = {}
        self.message = None
        
    
    
    async def post_button(self):
        channel = self.bot.get_channel(self.channel_id)
        if not channel:
            return
        
        await channel.purge(limit=1000)
        
        embed = disnake.Embed(
            title="Temporärer privater Voicechannel",
            description="Klicke auf den Button, um einen eigenen Voice-Channel zu erstellen!",
            color = 0x2ECC71
        )
        view = disnake.ui.View(timeout=None)
        view.add_item(disnake.ui.Button(
            label="Erstelle Voice-Channel",
            style=disnake.ButtonStyle.danger,
            custom_id="create_temp_vc"
        ))
        
        self.message = await channel.send(embed=embed, view=view)
        
    @commands.Cog.listener()
    async def on_button_click(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id != "create_temp_vc":
            return
        
        guild = inter.guild
        user = inter.author
        
        category = disnake.utils.get(guild.categories, name=self.category_name)
        if not category:
            category = await guild.create_category(self.category_name)
        
        vc = await guild.create_voice_channel(
            name=f"private {user.display_name}",
            category=category,
            user_limit=2,
        )
        self.temp_channels[user.id] = vc.id
        await inter.response.send_message(
            f"Dein privater Voice-Channel wurde erstellt: {vc.mention}",
            ephemeral=True
        )
        
        if user.voice:
            await user.move_to(vc)
            
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: disnake.Member, before: disnake.VoiceState, after: disnake.VoiceState):
        # deletee temp voice if empty
        if before.channel and before.channel.id in self.temp_channels.values():
            vc = before.channel
            if len(vc.members) == 0:
                await vc.delete()
                user_ids = [uid for uid, cid in self.temp_channels.items() if cid == vc.id]
                for uid in user_ids:
                    del self.temp_channels[uid]
                    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        await self.post_button()


def setup(bot: commands.Bot):
    bot.add_cog(TempVoice(bot, channel_id=VOICE_CREATE_CHANNEL_ID))