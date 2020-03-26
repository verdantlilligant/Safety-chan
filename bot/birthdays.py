from apscheduler.schedulers.asyncio import AsyncIOScheduler
from asyncio import Lock, sleep
from datetime import datetime, timedelta
from discord.ext import tasks, commands
from discord.ext.commands import Bot, Cog
from functools import cmp_to_key
from googleapiclient.discovery import build
from os import environ
from threading import Timer
from typing import List, Optional, Tuple
from tzlocal import get_localzone

seconds_in_year = 60 * 60 * 24 * 365.2425

def compare_people(a: Tuple[str, Optional[datetime]], b: Tuple[str, Optional[datetime]]):
  if a[1] is None and b[1] is None:
    return 0
  elif a[1] is None:
    return 1
  elif b[1] is None:
    return -1

  month_diff = a[1].month - b[1].month

  if month_diff != 0:
    return month_diff
  
  return a[1].day - b[1].day

def get_date(input: str) -> Optional[datetime]:
  try:
    return datetime.strptime(input, "%m/%d/%y")
  except ValueError:
    try:
      return datetime.strptime(input, "%m/%d/%Y")
    except ValueError:
      return None

def localtime(input: datetime, tz) -> datetime:
  return tz.normalize(tz.localize(input))

class BirthdayManager(Cog):
  def __init__(self, bot: Bot):
    self.birthdays: List[Tuple[str, Optional[datetime]]] = []
    self.bot = bot
    self.lock = Lock()
    self.timer: Optional[Timer] = None

    self.channel = int(environ.get("SAFETY_ANNOUNCEMENT_CHANNEL"))
    self.doc = environ.get("SAFETY_GOOGLE_DOCS_LINK")
    self.key = environ.get("SAFETY_GOOGLE_KEY")
    self.service = build("sheets", "v4", developerKey=self.key)
    
    self.refresh_birthdays.start()

    self.scheduler = AsyncIOScheduler()
    self.scheduler.add_job(self.schedule_birthday, trigger="cron", hour=0, minute=0, second=0)
    self.scheduler.start()

  def cog_unload(self):
    self.refresh_birthdays.cancel()
    self.scheduler.remove_all_jobs()

  @tasks.loop(hours=48)
  async def refresh_birthdays(self):
    async with self.lock:
      data = self.service.spreadsheets() \
        .values() \
        .get(spreadsheetId=self.doc, range="A2:J500") \
        .execute() \
        .get("values", [])

      self.birthdays.clear()

      for person in data:
        kerberos = person[1]
        birthday = person[9] if len(person) >= 10 else person[-1]
        self.birthdays.append((kerberos, get_date(birthday)))

      self.birthdays.sort(key=cmp_to_key(compare_people))

  async def schedule_birthday(self):
    async with self.lock:
      tz = get_localzone()

      now = datetime.now(tz)
      tomorrow = (now + timedelta(1)) \
        .replace(hour=0, minute=0, second=0, microsecond=0)

      people: List[Tuple[str, datetime]] = []

      for person in self.birthdays:
        if person[1] is None:
          continue

        current_birthday = localtime(person[1].replace(year=now.year), tz)
        
        if tomorrow - timedelta(1) <= current_birthday < tomorrow:
          people.append(person)

      if len(people) == 0:
        return

      names = [person[0] for person in people]
      names_str = ", ".join(names)
      message = f"Happy birthday to {names_str}!\n"

      for person in people:
        difference = tomorrow - localtime(person[1], tz)
        age = round(difference.total_seconds() / seconds_in_year)
        message += f"{person[0]} is {age} years old\n"

      target_channel = self.bot.get_channel(self.channel)

      while target_channel is None:
        await sleep(5)
        target_channel = self.bot.get_channel(self.channel)

      await target_channel.send(message)
