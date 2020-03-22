from asyncio import gather, sleep
from discord import Message
from discord.ext import commands
from discord.ext.commands import Bot, Cog, Context, command, CommandInvokeError
from discord.utils import get
from time import time

from typing import List, Tuple

emojis_order = [
  "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"
]

def vote_str(count: int) -> str:
  return "vote" if count == 1 else "votes"

class PollManager(Cog):
  def __init__(self, bot: Bot):
    self.bot = bot
    self.polls: List[Tuple[int, float, Message]] = []
    
  async def cog_command_error(self, ctx: Context, error: CommandInvokeError):
    """
    Handles errors for poll commands
    """
    await ctx.send(error.original)

  def should_remove(self, old_time: float, current_time: float, minutes: int) -> bool:
    return current_time - old_time >= minutes * 10

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

    poll = f"poll by {ctx.message.author.mention} ({timing} {time_msg}): **{topic}**\n\n```\n"

    for idx in range(len(options)):
      poll += f"{idx + 1}. {options[idx]}\n"

    message = await ctx.send(poll + "```")

    for idx in range(len(options)):
      await message.add_reaction(emojis_order[idx])

    await sleep(timing * 60)

    msg = await message.channel.fetch_message(message.id)
    
    lines = msg.content.split("\n")
  
    # remove the leading numbers (1., 10.)
    options = [
      line[line.index(".") + 2:] for line in lines[3:-1]
    ]

    results: List[Tuple[int, str]] = []

    for reaction in msg.reactions:
      try:
        index = emojis_order.index(reaction.emoji)
        results.append((reaction.count - 1, options[index]))
      except ValueError:
        pass

    results.sort(reverse=True)
    
    wins = [results[0][1]]
    max_count = results[0][0]

    for idx in range(1, len(results)):
      if results[idx][0] == max_count:
        wins.append(results[idx][1])
      else:
        break
    
    wins.sort()

    max_vote_msg = vote_str(max_count)
    result_msg = f"results of {lines[0]}:\n"

    if len(wins) > 1:
      joined_str = ", ".join(wins)
      result_msg += f"**Tie between {joined_str}** ({max_count} {max_vote_msg} each)\n\n>>> "
    else:
      result_msg += f"**{wins[0]}** wins! ({max_count} {max_vote_msg})\n\n>>> "

    for idx in range(len(wins), len(results)):
      vote_msg = vote_str(results[idx][0])
      result_msg += f"**{results[idx][1]}** ({results[idx][0]} {vote_msg})\n"

    await ctx.send(result_msg)
