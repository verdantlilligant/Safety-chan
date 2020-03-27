from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from dateutil.tz import tzlocal
from discord.channel import TextChannel
from discord.ext import commands
from discord.ext.commands import Bot, Cog, Context, CommandInvokeError
from redlock import RedLockFactory
from textwrap import dedent

import bot
from .util import get_local_date

async def register_event(channel_id: int, event: str, time: str, members=[]):
  message = dedent(f"""
  Time for {event}!
  {" ".join(members)} 
  """)
  channel = bot.bot.get_channel(channel_id)
  await channel.send(message)

factory = RedLockFactory([{
  "host": "127.0.0.1"
}])

class EventsManager(Cog):
  def __init__(self, bot: Bot):
    self.bot = bot
    self.scheduler = AsyncIOScheduler()
    self.scheduler.add_jobstore("redis")
    self.scheduler.start()

  async def cog_command_error(self, ctx: Context, error: CommandInvokeError):
    """
    Handles errors for poll commands
    """
    await ctx.send(error.original)

  @commands.guild_only()
  @commands.command()
  async def schedule(self, ctx: Context, event: str, time: str, timezone="EST5EDT"):
    """
    Schedule an event. Guild-only.

    This accepts the following formats:
    - AM/PM, with seconds: mm/dd/yy hh:mm:ss AM/PM (1/1/11 1:11:11 AM)
    - AM/PM, no seconds: mm/dd/yy hh:mm AM/PM (1/1/11 2:01 pm)
    - 24-hour, seconds: mm/dd/yy HH:mm:ss (01/1/13 13:13:13)
    - 24-hour, no seconds: mm/dd/yy HH:mm (1/01/13 08:27)
    """
    scheduled_date = get_local_date(time)
    now = datetime.now(tzlocal())
    wait = (scheduled_date - now)
    
    job = self.scheduler.add_job(register_event, 'date', run_date=scheduled_date, args=[
      ctx.channel.id, event, time, [ctx.message.author.mention]
    ])
    
    msg = dedent(f"""
    {event} by {ctx.message.author.mention} for {time} ({wait} from now)
    Sign up with the id **{job.id}**
    """)

    await ctx.send(msg)

  @commands.command()
  async def signup(self, ctx: Context, jobid: str):
    added = False
    author = ""
    channel = None
    event = ""
    time = ""

    with factory.create_lock(jobid):
      job = self.scheduler.get_job(jobid)

      if job is None:
        raise ValueError(f"The job {jobid} does not exist")

      channel = self.bot.get_channel(job.args[0])

      if channel is None or not ctx.message.author in channel.members:
        raise ValueError(f"The job {jobid} does not exist")

      new_member = ctx.message.author.mention
      author = job.args[3][0]
      event = job.args[1]
      time = job.args[2]

      if new_member not in job.args[3]:
        members = job.args[3] + [new_member]
        new_args = job.args[0:3] + (members,)
        job.modify(args=new_args)
        added = True
    
    if added:
      await channel.send(f"{ctx.message.author.mention} has signed up for {event} at {time} by {author}")
    else:
      await ctx.message.author.send(f"You have already signed up for {event} at {time} by {author}")
