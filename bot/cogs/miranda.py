#miranda.py
#Sibyl-chan will read you your Miranda rights (not that she believes you have any).

from discord import TextChannel
from discord.ext.commands import Bot, Cog, Context, command, is_owner

__all__ = ["MirandaManager"]

class MirandaManager(Cog):
  def __init__(self, bot: Bot):
    self.bot = bot

  @is_owner()
  @command()
  async def sibyl(self, ctx: Context, channel: TextChannel):
    await channel.send(f"```You have the right to remain silent. Anything you say will be used against you.```")