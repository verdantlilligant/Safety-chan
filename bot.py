from discord import Member, Role, User
from discord.ext.commands import Bot, CommandInvokeError, Context, Converter, Greedy

from roles import RolesManager

bot = Bot(command_prefix='>')
bot.add_cog(RolesManager(bot))
