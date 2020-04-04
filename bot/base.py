from discord.ext.commands import Bot, Cog, Context, CommandInvokeError

__all__ = ["CustomCog"]

class CustomCog(Cog):
  async def cog_command_error(self, ctx: Context, error: Exception):
    """
    Handles errors for custom cogs
    """
    if isinstance(error, CommandInvokeError):
      await ctx.send(error.original)
    else:
      await ctx.send(error)