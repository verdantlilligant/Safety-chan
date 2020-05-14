from discord import TextChannel
from discord.ext.commands import Bot, Cog, Context, command

__all__ = ["CreditManager"]

class CreditManager(cog):
    def __init__(self, bot: Bot):
        self.bot = bot
    
    @command()