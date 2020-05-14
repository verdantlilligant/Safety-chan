from discord import Member, Role, User
from discord.ext.commands import Bot, CommandInvokeError, DefaultHelpCommand, Context, Converter, Greedy

from .cogs import SibylManager, RolesManager

__all__ = ["bot"]

bot = Bot(command_prefix='!', help_command=DefaultHelpCommand(dm_help=True))


bot.add_cog(SibylManager(bot))
bot.add_cog(StatusManager(bot))