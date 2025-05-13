import discord
from discord.ext import commands
from discord.ui import Button, View

class minigame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='avt')
    async def profile(self, ctx, member: discord.Member = None ):
        member = member or ctx.author

        user = await self.bot.fetch_user(member.id)
        avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
        banner_url = user.banner.url if user.banner else "No banner"

        embed = discord.Embed(
            title=f"Hồ sơ của {member.name}",
            color=discord.Color.blue()
        )
        embed.set_image(url=avatar_url)

        avatar_button = Button(label="Avatar", style=discord.ButtonStyle.primary)
        banner_button = Button(label="Banner", style=discord.ButtonStyle.primary)

        async def avatar_callback(interaction):
            embed.set_image(url=avatar_url)
            await interaction.response.edit_message(embed=embed)

        async def banner_callback(interaction):
            if banner_url != "No banner":
                embed.set_image(url=banner_url)
            else:
                embed.set_image(url="") 
                embed.description = "User does not have a banner."
            await interaction.response.edit_message(embed=embed)

        avatar_button.callback = avatar_callback
        banner_button.callback = banner_callback

        view = View(timeout=None)
        view.add_item(avatar_button)
        view.add_item(banner_button)

        await ctx.send(embed=embed, view=view)

    @commands.command(name='ping')
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)  # Convert latency to milliseconds
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Latency: {latency}ms",
            color=discord.Color.green()
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(minigame(bot))
