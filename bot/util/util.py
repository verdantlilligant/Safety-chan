from datetime import datetime
from dateutil.parser import parse
from dateutil.tz import tzlocal, tzstr
from typing import List, Optional

__all__ = ["get_date", "get_local_date"]

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
  """
  Parses a date given a list of possible string formats.
  The formats are parsed from left to right, accepting the first format that works.

  Args:
    input (str): the string to parse
    formats (List[str]): a list of time formats

  Returns:
    a datetime representing the time, or None if all fo the formats fail
  """
  for format in formats:
    try:
      return datetime.strptime(input, format)
    except ValueError:
      pass
  
  return None

def get_local_date(input: str) -> Optional[datetime]:
  """
  Parses a date string with a time zone and converts it to server local time.
  If the string cannot be parsed, returns None

  Args:
    input (str): an input string with time zone string (%Z)

  Returns:
    a datetime representing the time converted to server local time
    or None if the parse fails
  """
  try:
    return parse(input, tzinfos=us_timezones).astimezone(tzlocal())
  except:
    return None
