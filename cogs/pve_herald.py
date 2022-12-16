from discord.ext import commands, tasks
from discord.ext.commands import Context
import requests


class PveHerald(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

