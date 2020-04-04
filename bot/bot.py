from discord import Member, Role, User
from discord.ext.commands import Bot, CommandInvokeError, DefaultHelpCommand, Context, Converter, Greedy

from .cogs import BirthdayManager, EventsManager, PollManager, RolesManager, RollManager, StatusManager

__all__ = ["bot"]

bot = Bot(command_prefix='>', help_command=DefaultHelpCommand(dm_help=True))

bot.add_cog(BirthdayManager(bot))
bot.add_cog(EventsManager(bot))
bot.add_cog(PollManager(bot))
bot.add_cog(RolesManager(bot))
bot.add_cog(RollManager(bot))
bot.add_cog(StatusManager(bot))