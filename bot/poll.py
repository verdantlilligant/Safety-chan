from discord.ext import commands
from discord.ext.commands import Cog, Context, command, CommandInvokeError
from discord.utils import get

emojis_order = [
  "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"
]

class PollManager(Cog):
  def __init__(self, bot):
    self.bot = bot

  async def cog_command_error(self, ctx: Context, error: CommandInvokeError):
    """
    Handles errors for poll commands
    """
    await ctx.send(error.original)

  @commands.command()
  async def poll(self, ctx, topic: str, timing: int, *options):
    """
    Creates an emoji-based poll for a certain topic.
    NOTE: It is important that statements involving multiple words are quoted if you want them to be together.
    
    Correct poll:
    >poll "What are birds?" 1 ":jeff:" "We don't know" (two options, ":jeff:" and "We don't know")
    
    Incorrect poll:
    >poll "What are birds?" 1 ":jeff:" We don't know (four options, ":jeff:", "We", "don't", and "know")

    Args:
      topic (str): The topic of this poll
      timing (int): How long this poll should last in minutes (currently unused)
      options (Tuple[str]): A list containing all the options. Currently, we handle up to 10.

    Raises:
      ValueError: if the input is malformed (no options, invalid time, > 10 options)
    """
    if len(options) < 1:
      raise ValueError("Please provide at least one option")

    if timing < 1:
      raise ValueError("You must wait at least one minute for a poll")

    if len(options)  > len(emojis_order):
      raise ValueError(f"I can only deal with up to {len(emojis_order)} options")

    time_msg = "minutes" if timing > 1 else "minute"

    poll = f"Poll by {ctx.message.author.mention} ({timing} {time_msg}): **{topic}**\n\n```"

    for idx in range(len(options)):
      poll += f"{idx + 1}. {options[idx]}\n"

    message = await ctx.send(poll + "```")

    for idx in range(len(options)):
      await message.add_reaction(emojis_order[idx])
