from discord import Member, Role, User
from discord.ext.commands import Bot, CommandInvokeError, DefaultHelpCommand, Context, Converter, Greedy

from .cogs import SibylManager, StatusManager, CreditManager, ReportManager, FineManager, RewardManager, 
AdjustManager, MirandaManager, HandoutManager

__all__ = ["bot"]

bot = Bot(command_prefix='!', help_command=DefaultHelpCommand(dm_help=True))

bot.add_cog(SibylManager(bot))
bot.add_cog(StatusManager(bot))
bot.add_cog(CreditManager(bot))
bot.add_cog(ReportManager(bot))
bot.add_cog(FineManager(bot))
bot.add_cog(RewardManager(bot))
bot.add_cog(AdjustManager(bot))
bot.add_cog(MirandaManager(bot))
bot.add_cog(HandoutManager(bot))
