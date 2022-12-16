from discord.ext import commands, tasks
from discord.ext.commands import Context
import requests
import datetime

class PveHerald(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = self.fetch_data()

    def fetch_data(self):
        # required to receive json response
        headers = {'x-herald-api': 'minified'}
        response = requests.get('https://eden-daoc.net/hrald/proxy.php?pve', headers=headers)

        return response.json()

    def parse_boss_kills(self):
        boss_kill_timer_map = {}
        for boss in self.data:
            last_killed_time = datetime.datetime.strptime(boss['killed_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
            try:
                boss_kill_timer_map[boss] = last_killed_time
            except TypeError:
                print("Found weird data")

        return boss_kill_timer_map
