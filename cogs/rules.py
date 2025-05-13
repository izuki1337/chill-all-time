import discord
from discord.ext import commands
from discord.ui import Button, View


class Rules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="rules", description="Luật server Discord / Discord server rules")
    async def help_command(self, ctx: commands.Context):
        embed = discord.Embed(
            title="Luật Discord Server / Discord Server Rules",
            color=discord.Color.dark_gray()  # Changed from blue to dark_gray
        )
        embed.add_field(
            name="Các luật discord không được vi phạm",
            value=(
                "1. Không spam chat - (**nên nói chuyện một cách văn minh**)\n"
                "2. Không đăng ảnh 18+, video có chứa nội dung đồ trụy không phù hợp với độ tuổi (hoặc đủ rồi thì ||trong sáng lên||)\n"
                "3. Không đăng link sever khác vào sever mình\n"
                "4. Không phân biệt chủng tộc, vùng miền\n"
                "5. Không xúc phạm thành viên khác\n"
                "6. Không chửi bới, toxic\n"
                "7. Không đăng thông tin cá nhân của người khác\n"
                "8. Không gây war - (khi cả ở trong voice và lẫn ở khu vực chat)\n"
            ),
            inline=False
        )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1248576973001719869/1333202218945347604/images.png?ex=679808d2&is=6796b752&hm=d0a0916c54c8c5e971cbbd3072aeb961e6984933ee41bae342b90605abc3489d&")
        embed.set_footer(
            text="Support server: https://discord.gg/j9XBApwznn",
            icon_url="https://cdn.discordapp.com/emojis/1269233177831145588.webp?size=80"
        )
        # Add the new GIF as thumbnail
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1235962216134742098/1259327208510586880/D47A6852-F8F4-4046-8A13-E635F0E9872B-1.gif?ex=67ef3c5b&is=67edeadb&hm=08a96564560a448c0b525e72ad9cfddd98ed9dabc857ff66e76a5df7a3d3b8b7&")
        info_button = Button(label="Thông tin thêm", style=discord.ButtonStyle.secondary)


        async def info_callback(interaction: discord.Interaction):
            info_embed = discord.Embed(
                title="Thông tin bổ sung / Additional Information",
                color=discord.Color.purple()
            )
            info_embed.add_field(
                name="Lưu ý quan trọng",
                value=(
                    "• Vi phạm các quy tắc có thể dẫn đến cảnh cáo hoặc cấm tùy theo mức độ nghiêm trọng\n"
                    "• Nếu bạn thấy ai đó vi phạm quy tắc, vui lòng báo cáo cho quản trị viên\n"
                    "• Các quy tắc có thể được cập nhật bất kỳ lúc nào, vui lòng kiểm tra thường xuyên\n"
                ),
                inline=False
            )
            info_embed.set_footer(
                text="Cảm ơn bạn đã đọc và tuân thủ quy tắc của server!",
                icon_url="https://cdn.discordapp.com/emojis/1332485373829451776.webp?size=80"
            )
            await interaction.response.send_message(embed=info_embed, ephemeral=True)


        info_button.callback = info_callback
        view = View(timeout=None)
        view.add_item(info_button)


        await ctx.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(Rules(bot))
