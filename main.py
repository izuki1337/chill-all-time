import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', intents=intents, help_command=None)

async def load_extensions():
    initial_extensions = [
        'cogs.rules', 
        'cogs.help', 
        'cogs.trangthai', 
        'cogs.combined',
        'cogs.minigame',
        'cogs.RoleList',
        'cogs.slash',
        'cogs.bot_AI' 
    ]
    
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
        except Exception as e:
            print(f"Failed to load extension {extension}: {e}")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print('------')

async def main():
    async with bot:
        await load_extensions()
        token = os.getenv('TOKEN')
        if token is None:
            raise ValueError("No TOKEN found in environment variables. Please check your .env file.")
        await bot.start(token)

if __name__ == '__main__':
    asyncio.run(main())


