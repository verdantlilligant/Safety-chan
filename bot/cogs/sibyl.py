from discord import TextChannel
from discord.ext.commands import Bot, Cog, Context, command, is_owner

__all__ = ["SibylManager"]

class SibylManager(Cog):
  def __init__(self, bot: Bot):
    self.bot = bot

  @is_owner()
  @command()
  async def impersonate(self, ctx: Context, channel: TextChannel, msg: str):
    await channel.send(f"```{msg}```")