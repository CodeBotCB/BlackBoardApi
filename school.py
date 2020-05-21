from datetime import date
from .bb_api import BlackBoardAPI
from redbot.core import Config
import schedule
from redbot.core import commands


class School(commands.Cog):
    """My custom cog"""
    '''def __init__(self):
        self.config = Config.get_conf(self, identifier=1234567890)
        default_global = {
            "name": "Unknown"
        }
        self.config.register_global(**default_global)
    '''

    @commands.command()
    async def get_tutor_link(self, ctx):
        # link for tutor pre-filled
        # https://docs.google.com/forms/d/e/1FAIpQLScckX09i7Dfv27_k1On8-GlkrB8OOF1l8twY9u_OeGzLc7u6Q/viewform?usp=pp_url&entry.814127073=2020-05-09&entry.1520997077=Chase
        # 2020-05-09
        today = date.today().strftime('%Y-%m-%d')
        await ctx.send("https://docs.google.com/forms/d/e/1FAIpQLScckX09i7Dfv27_k1On8-GlkrB8OOF1l8twY9u_OeGzLc7u6Q/viewform?usp=pp_url&entry.814127073={0}".format(today))

    @commands.command()
    async def get(self, ctx, *, text): # text can be poop. I use text cause it makes sense. You don't have to make sense.
        await ctx.send(text)

    @commands.command()
    async def set_daily_homework_reminders(self, ctx, ):
        schedule.every().day.at()