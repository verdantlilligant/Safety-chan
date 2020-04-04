"""
Represents our shared scheduler and distributed locks
The scheduler is backed by redis, meaning that jobs can be restored after a restart
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from redlock import RedLockFactory

__all__ = ["redlocks", "scheduler"]

scheduler = AsyncIOScheduler()
scheduler.add_jobstore("redis")

redlocks = RedLockFactory([{
  "host": "127.0.0.1"
}])


scheduler.start()