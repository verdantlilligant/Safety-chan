from bot import bot
import os

if "SAFETY_BOT_TOKEN" not in os.environ:
  print("No Bot token provided", file=os.sys.stderr)
  os.sys.exit(-1)

bot.run(os.environ["SAFETY_BOT_TOKEN"])
