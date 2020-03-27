from datetime import datetime
from dateutil.parser import parse
from dateutil.tz import tzlocal, tzstr
from typing import List, Optional

us_timezones = {
  "EDT": -14400,
  "EST": tzstr("EST5EDT"),
  "CDT": -18000,
  "CST": tzstr("CST6CDT"),
  "MDT": -21600,
  "MST": tzstr("MST7MDT"),
  "PDT": -25200,
  "PST": tzstr("PST6PDT"),
  "AKDT": -28800,
  "AKST": tzstr("AKST9AKDT")
}

def get_date(input: str, formats: List[str]) -> Optional[datetime]:
  for format in formats:
    try:
      return datetime.strptime(input, format)
    except ValueError:
      pass
  
  return None

def get_local_date(input: str) -> Optional[datetime]:
  try:
    return parse(input, tzinfos=us_timezones).astimezone(tzlocal())
  except:
    return None
