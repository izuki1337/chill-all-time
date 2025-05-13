import discord
from discord.ext import commands
from discord import app_commands
import random
import datetime

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Kiểm tra độ trễ của bot")
    async def ping(self, interaction: discord.Interaction):
        start_time = datetime.datetime.now()
        message = await interaction.response.send_message("Pinging...")
        end_time = datetime.datetime.now()

    @app_commands.command(name="8ball", description="Hỏi câu hỏi yes/no")
    async def eightball(self, interaction: discord.Interaction, question: str):
        responses = ["Có", "Không", "Có thể", "Chắc chắn rồi", "Không chắc lắm", "Hỏi lại sau", "Đừng hy vọng"]
        await interaction.response.send_message(f"🎱 **Câu hỏi:** {question}\n**Trả lời:** {random.choice(responses)}")

    @app_commands.command(name="roll", description="Tung xúc xắc")
    async def roll(self, interaction: discord.Interaction, sides: int = 6):
        result = random.randint(1, sides)
        await interaction.response.send_message(f"🎲 Bạn tung được số: {result}")

    @app_commands.command(name="poll", description="Tạo một cuộc thăm dò")
    async def poll(self, interaction: discord.Interaction, question: str, option1: str, option2: str):
        embed = discord.Embed(title="📊 Thăm dò ý kiến", description=question, color=discord.Color.blue())
        embed.add_field(name="1️⃣", value=option1, inline=True)
        embed.add_field(name="2️⃣", value=option2, inline=True)
        message = await interaction.response.send_message(embed=embed)
        message = await interaction.original_response()
        await message.add_reaction("1️⃣")
        await message.add_reaction("2️⃣")

async def setup(bot):
    await bot.add_cog(Slash(bot))
    print("Slash commands cog loaded successfully!")