import discord
from discord.ext import commands
from discord.ui import Button, View

class RoleList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="roles", description="Hiển thị danh sách các vai trò của máy chủ được sắp xếp thành các danh mục.")
    async def roles(self, ctx):
        """Hiển thị danh sách các vai trò của máy chủ được sắp xếp thành các danh mục với giải thích và nút."""
        roles = ctx.guild.roles
        roles = sorted(roles, key=lambda r: r.position, reverse=True)  # Sắp xếp vai trò theo vị trí

        # Define the role categories and explanations
        manager_roles = ["owner👑", "trưởng làng🎃", "Moderator", "staff⭐", "Bot"]
        special_roles = ["✨Nhà tài trợ✨", "Server Booster", "Donate+", "Donate", "tk víp bro"]
        common_roles = ["dân làng 💯", "FAで", "Giveaway Ping🎉", "Ping xàm"]

        explanations = {
            "owner👑": "Quyền lực tối cao trong máy chủ.",
            "trưởng làng🎃": "Người chủ quản làng, giám sát các hoạt động.",
            "Moderator": "Chịu trách nhiệm duy trì trật tự.",
            "staff⭐": "Hỗ trợ quản lý máy chủ.",
            "Bot": "Trợ lý tự động với các nhiệm vụ khác nhau.",
            "✨Nhà tài trợ✨": "Những người ủng hộ đóng góp cho máy chủ.",
            "Server Booster": "Người dùng tăng cường máy chủ.",
            "Donate+": "Những người đóng góp cao cấp.",
            "Donate": "Những người đóng góp giúp đỡ máy chủ.",
            "tk víp bro": "Thành viên VIP với các đặc quyền đặc biệt.",
            "dân làng 💯": "Thành viên thường của máy chủ.",
            "FAで": "Độc thân và sẵn sàng kết bạn!",
            "Giveaway Ping🎉": "Nhận thông báo cho các sự kiện tặng quà.",
            "Ping xàm": "Vai trò thông báo chung."
        }

        def get_role_explanation(role):
            role_name = role.name.strip()
            return explanations.get(role_name, "Không có giải thích cho vai trò này.")

        # Filter roles to only include those in the predefined lists
        manager_list = [f"{role.mention} - {get_role_explanation(role)}" for role in roles if role.name in manager_roles]
        special_list = [f"{role.mention} - {get_role_explanation(role)}" for role in roles if role.name in special_roles]
        common_list = [f"{role.mention} - {get_role_explanation(role)}" for role in roles if role.name in common_roles]

        embed = discord.Embed(
            title=" THÔNG TIN VAI TRÒ ",
            color=discord.Color.dark_gray()  # Changed from blue to dark_gray
        )

        embed.add_field(
            name="⚔️ Vai Trò Quản Lý ⚔️",
            value=f"![Manager Roles](https://cdn.discordapp.com/emojis/1335031535119761510.webp?size=80)\n" + ("\n".join(manager_list) if manager_list else "Không có vai trò nào"),
            inline=False
        )

        embed.add_field(
            name="✨ Vai Trò Đặc Biệt ✨",
            value=f"![Special Roles](https://cdn.discordapp.com/emojis/1335031537724555314.webp?size=80)\n" + ("\n".join(special_list) if special_list else "Không có vai trò nào"),
            inline=False
        )

        embed.add_field(
            name="⚙️ Vai Trò Chung ⚙️",
            value=f"![Common Roles](https://cdn.discordapp.com/emojis/1335031533119078480.webp?size=80)\n" + ("\n".join(common_list) if common_list else "Không có vai trò nào"),
            inline=False
        )

        banner_url = "https://cdn.discordapp.com/attachments/1333215931387875378/1335028913801265263/roles.png?ex=679eae10&is=679d5c90&hm=ecf6a7334da79852a539a541ec1ca8aa8a07d17e704ef518570b87a1412366bd&"  # Thay bằng URL banner thực tế của bạn
        embed.set_image(url=banner_url)
        
        # Add the new GIF as thumbnail
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1235962216134742098/1259327208510586880/D47A6852-F8F4-4046-8A13-E635F0E9872B-1.gif?ex=67ef3c5b&is=67edeadb&hm=08a96564560a448c0b525e72ad9cfddd98ed9dabc857ff66e76a5df7a3d3b8b7&")

        # Define buttons
        giveaway_ping_button = Button(label="Giveaway Ping🎉", style=discord.ButtonStyle.primary)
        ping_xam_button = Button(label="Ping xàm", style=discord.ButtonStyle.primary)
        fa_button = Button(label="FAで", style=discord.ButtonStyle.primary)

        async def giveaway_ping_callback(interaction):
            role = discord.utils.get(ctx.guild.roles, name="Giveaway Ping🎉")
            if role:
                if role in interaction.user.roles:
                    await interaction.user.remove_roles(role)
                    await interaction.response.send_message("Đã hủy nhận vai trò Giveaway Ping.", ephemeral=True)
                else:
                    await interaction.user.add_roles(role)
                    await interaction.response.send_message("Đã nhận vai trò Giveaway Ping.", ephemeral=True)
            else:
                await interaction.response.send_message("Vai trò không tồn tại.", ephemeral=True)

        async def ping_xam_callback(interaction):
            role = discord.utils.get(ctx.guild.roles, name="Ping xàm")
            if role:
                if role in interaction.user.roles:
                    await interaction.user.remove_roles(role)
                    await interaction.response.send_message("Đã hủy nhận vai trò Ping xàm.", ephemeral=True)
                else:
                    await interaction.user.add_roles(role)
                    await interaction.response.send_message("Đã nhận vai trò Ping xàm.", ephemeral=True)
            else:
                await interaction.response.send_message("Vai trò không tồn tại.", ephemeral=True)

        async def fa_callback(interaction):
            role = discord.utils.get(ctx.guild.roles, name="FAで")
            if role:
                if role in interaction.user.roles:
                    await interaction.user.remove_roles(role)
                    await interaction.response.send_message("Đã hủy nhận vai trò FAで.", ephemeral=True)
                else:
                    await interaction.user.add_roles(role)
                    await interaction.response.send_message("Đã nhận vai trò FAで.", ephemeral=True)
            else:
                await interaction.response.send_message("Vai trò không tồn tại.", ephemeral=True)

        giveaway_ping_button.callback = giveaway_ping_callback
        ping_xam_button.callback = ping_xam_callback
        fa_button.callback = fa_callback

        view = View(timeout=None)
        view.add_item(giveaway_ping_button)
        view.add_item(ping_xam_button)
        view.add_item(fa_button)

        await ctx.send(embed=embed, view=view, allowed_mentions=discord.AllowedMentions.none())  # Tắt ping

async def setup(bot):
    await bot.add_cog(RoleList(bot))
