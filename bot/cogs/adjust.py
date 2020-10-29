#set credit score

from discord import TextChannel
from discord.ext.commands import Bot, Cog, Context, command, is_owner

class AdjustManager(cog):
    def __init__(self, bot: Bot):
        self.bot = bot
    
    @command()
    async def sibyl(self, ctx: Context, channel: TextChannel, msg: str):
        await channel.send(f"")