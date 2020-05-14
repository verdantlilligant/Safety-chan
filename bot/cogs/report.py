#report citizens for misbehaving

class ReportManager(cog):
    def __init__(self, bot: Bot):
        self.bot = bot
    
    @command()