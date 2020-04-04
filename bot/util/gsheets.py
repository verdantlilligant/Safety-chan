from googleapiclient.discovery import build
from os import environ

__all__ = ["sheets"]

key = environ.get("SAFETY_GOOGLE_KEY")
sheets = build("sheets", "v4", developerKey=key)
    