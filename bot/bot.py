from discord import Member, Role, User
from discord.ext.commands import Bot, CommandInvokeError, DefaultHelpCommand, Context, Converter, Greedy

from .birthdays import BirthdayManager
from .poll import PollManager
from .roles import RolesManager
from .roll import RollManager

bot = Bot(command_prefix='>', help_command=DefaultHelpCommand(dm_help=True))

bot.add_cog(BirthdayManager(bot))
bot.add_cog(PollManager(bot))
bot.add_cog(RolesManager(bot))
bot.add_cog(RollManager(bot))
