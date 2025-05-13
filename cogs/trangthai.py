import discord
import random
from discord.ext import commands, tasks
from datetime import datetime
import asyncio

class TrangThai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.now()
        self.status_messages = ["o_0 nah why you look me?"]
        self.message_index = 0
        self.update_status.start()

    @tasks.loop(seconds=20)
    async def update_status(self):
        current_time = datetime.now()
        uptime = current_time - self.start_time 
        hours, remainder = divmod(uptime.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)

        status_message = self.status_messages[self.message_index]
        activity = discord.Activity(type=discord.ActivityType.watching, name=status_message)
        await self.bot.change_presence(status=discord.Status.idle, activity=activity)

        self.message_index = (self.message_index + 1) % len(self.status_messages)

    @update_status.before_loop
    async def before_update_status(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        # Remove this line as it's causing command processing duplication
        # await self.bot.process_commands(message)

        if self.bot.user.mentioned_in(message) and "@everyone" not in message.content and "@here" not in message.content:
            embed = discord.Embed(
                title="Tại sao bạn lại tag tôi?",
                description="**Bot được làm bởi một thg sadboy và một con mèo béo trong lúc ngồi voice** | **( ͡° ͜ʖ ͡°)**",
                color=discord.Color.dark_gray()
            )
            embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1335385233213886475.webp?size=80")
            embed.add_field(name="Tên bot", value=self.bot.user.name, inline=True)
            embed.add_field(name="ID bot", value=self.bot.user.id, inline=True)
            embed.add_field(name="Prefix", value="$", inline=True)
            embed.add_field(name="Server me", value="`discord.gg/AGygM9dV`", inline=True)
            icon_url = "https://cdn.discordapp.com/emojis/776055210060808222.webp?size=80"
            embed.set_footer(text="______________END________________", icon_url=icon_url)

            msg = await message.channel.send(embed=embed)
            await asyncio.sleep(20)
            await msg.delete()
            await message.delete()

    @commands.Cog.listener()
    async def on_ready(self):
        print('_________________________')
        print('YO BRO no SIMP GAI NHE')
        print('__________________________')

async def setup(bot):
    await bot.add_cog(TrangThai(bot))
