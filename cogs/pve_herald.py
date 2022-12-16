from discord.ext import commands, tasks
from helpers import db_manager
import aiohttp
import datetime
import discord


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

    async def parse_boss_kills(self):
        boss_kill_timer_map = {}
        for boss in await self.data:
            last_killed_time = datetime.datetime.strptime(boss['killed_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
            try:
                boss_kill_timer_map[boss] = last_killed_time
            except TypeError:
                print("Found weird data")

        return boss_kill_timer_map

    @tasks.loop(minutes=5.0)
    async def report_boss_kills(self):
        pass

    @commands.hybrid_command(
        name="setchannel",
        description="Sets channel to report boss kills in.",
    )
    async def set_reporting_channel(self, context: commands.Context, channel: discord.TextChannel):
        if await db_manager.get_channel(context.guild.id):
            await db_manager.update_channel(context.guild.id, channel.id)
        else:
            await db_manager.add_channel(context.guild.id, channel.id)

        user_confirmation_message = discord.Embed(
            description="The channel has been set.",
            color=0x9C84EF
        )
        new_channel_embed = discord.Embed(
            description="This has been set as the default channel for boss kill updates.",
            color=0x9C84EF
        )

        await context.send(embed=user_confirmation_message, ephemeral=True)
        await channel.send(embed=new_channel_embed)

async def setup(bot):
    await bot.add_cog(PveHerald(bot))
