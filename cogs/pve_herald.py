from discord.ext import commands, tasks
from discord.ext.commands import Context
import aiohttp
import datetime

class PveHerald(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = self.fetch_data()
        self.boss_kill_times = self.parse_boss_kills()

    async def fetch_data(self):
        # required to receive json response
        headers = {'x-herald-api': 'minified'}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get('https://eden-daoc.net/hrald/proxy.php?pve') as request:
                if request.status == 200:
                    data = await request.json()
                    return data
                else:
                    print("Could not fetch data")
    def parse_boss_kills(self):
        boss_kill_timer_map = {}
        for boss in self.data:
            last_killed_time = datetime.datetime.strptime(boss['killed_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
            try:
                boss_kill_timer_map[boss] = last_killed_time
            except TypeError:
                print("Found weird data")

        return boss_kill_timer_map

    @tasks.loop(minutes=5.0)
    def report_boss_kills(self):
        pass