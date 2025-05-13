import discord
from discord.ext import commands
from discord.ui import Select, View, Button

class HelpView(View):
    def __init__(self):
        super().__init__(timeout=None)
        
        # Admin button
        self.add_item(Button(
            label="Admin Commands",
            style=discord.ButtonStyle.red,
            custom_id="admin_commands"
        ))
        
        # User button
        self.add_item(Button(
            label="User Commands",
            style=discord.ButtonStyle.green,
            custom_id="user_commands"
        ))
        
        # AI Setup button
        self.add_item(Button(
            label="AI Setup",
            style=discord.ButtonStyle.blurple,
            custom_id="ai_setup"
        ))

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    async def help(self, ctx):
        admin_embed = discord.Embed(
            title="📜 Trợ Giúp - Admin Commands 📜",
            description="Các lệnh dành cho quản trị viên",
            color=discord.Color.pink()
        )
        admin_embed.add_field(
            name="👢 `.kick` @người dùng [lý do]",
            value="Đá một người dùng ra khỏi máy chủ.",
            inline=False
        )
        admin_embed.add_field(
            name="🚫 `.ban` @người dùng [lý do]",
            value="Cấm một người dùng khỏi máy chủ.",
            inline=False
        )
        admin_embed.add_field(
            name="🔓 `.unban` tên người dùng#1234",
            value="Gỡ cấm một người dùng đã bị cấm trước đó.",
            inline=False
        )
        admin_embed.add_field(
            name="🔇 `.mute` @người dùng thời gian [lý do]",
            value="Chặn tiếng một người dùng trong khoảng thời gian nhất định bằng giây.",
            inline=False
        )
        admin_embed.add_field(
            name="🔊 `.unmute` @người dùng",
            value="Bỏ chặn tiếng một người dùng đã bị chặn trước đó.",
            inline=False
        )
        admin_embed.add_field(
            name="🎭 `.giverole` @người dùng @vai trò",
            value="Gán một vai trò nhất định cho người dùng.",
            inline=False
        )
        admin_embed.add_field(
            name="⚔️ `.roles`",
            value="Hiển thị danh sách các vai trò của máy chủ được sắp xếp thành các danh mục với giải thích và nút.",
            inline=False
        )
        admin_embed.add_field(
            name="🧹 `.clear` số lượng",
            value="Xóa một số lượng tin nhắn trong kênh hiện tại.",
            inline=False
        )

        user_embed = discord.Embed(
            title="📜 Trợ Giúp - User Commands 📜",
            description="Các lệnh dành cho thành viên",
            color=discord.Color.pink()
        )
        user_embed.add_field(
            name="🏓 `.ping`",
            value="Kiểm tra độ trễ của bot.",
            inline=False
        )
        user_embed.add_field(
            name="🖼️ `.avt` [@người dùng]",
            value="Hiển thị avatar của bạn hoặc người dùng được chỉ định.",
            inline=False
        )
        user_embed.set_footer(text="[] = không bắt buộc | <> = bắt buộc")

        # New AI setup embed
        ai_embed = discord.Embed(
            title="🤖 Hướng Dẫn Thiết Lập AI 🤖",
            description="Cách thiết lập và sử dụng tính năng AI chat",
            color=discord.Color.blue()
        )
        ai_embed.add_field(
            name="🔧 `.add_channel` [#kênh]",
            value="Thêm kênh hiện tại hoặc kênh được chỉ định vào danh sách kênh AI. Bot sẽ tự động trả lời mọi tin nhắn trong kênh này. (Chỉ Admin)",
            inline=False
        )
        ai_embed.add_field(
            name="❌ `.remove_channel` [#kênh]",
            value="Xóa kênh hiện tại hoặc kênh được chỉ định khỏi danh sách kênh AI. (Chỉ Admin)",
            inline=False
        )
        ai_embed.add_field(
            name="📋 `.list_channels`",
            value="Hiển thị danh sách các kênh AI đã được thiết lập.",
            inline=False
        )
        ai_embed.add_field(
            name="💬 Cách sử dụng AI",
            value="Có 3 cách để trò chuyện với AI:\n"
                 "1. Gửi tin nhắn trong kênh AI đã thiết lập\n"
                 "2. Mention bot: `@tên_bot câu hỏi của bạn`\n"
                 "3. Sử dụng prefix: `hỏi câu hỏi của bạn` hoặc `ai: câu hỏi của bạn`",
            inline=False
        )
        ai_embed.set_footer(text="[] = không bắt buộc | <> = bắt buộc")

        avatar_url = "https://cdn.discordapp.com/emojis/856362922720231514.gif?size=48"
        
        view = HelpView()
        
        async def admin_button_callback(interaction: discord.Interaction):
            if interaction.user.guild_permissions.administrator:
                admin_embed.set_thumbnail(url=avatar_url)
                await interaction.response.edit_message(embed=admin_embed)
            else:
                await interaction.response.send_message("Bạn không có quyền xem lệnh admin!", ephemeral=True)

        async def user_button_callback(interaction: discord.Interaction):
            user_embed.set_thumbnail(url=avatar_url)
            await interaction.response.edit_message(embed=user_embed)
            
        async def ai_button_callback(interaction: discord.Interaction):
            ai_embed.set_thumbnail(url=avatar_url)
            await interaction.response.edit_message(embed=ai_embed)

        view.children[0].callback = admin_button_callback  # Admin button
        view.children[1].callback = user_button_callback   # User button
        view.children[2].callback = ai_button_callback     # AI Setup button

        # Initial embed
        initial_embed = user_embed
        if ctx.author.guild_permissions.administrator:
            initial_embed = admin_embed
        initial_embed.set_thumbnail(url=avatar_url)

        await ctx.send(embed=initial_embed, view=view)

async def setup(bot):
    await bot.add_cog(Help(bot))


# In your help cog, add a section for AI commands

@commands.command(name="help_ai")
async def help_ai(self, ctx):
    """Hiển thị hướng dẫn sử dụng AI"""
    embed = discord.Embed(
        title="🤖 Hướng dẫn sử dụng AI",
        description="Dưới đây là các cách để tương tác với AI:",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="💬 Trò chuyện trong kênh AI",
        value="Trong các kênh AI, mọi tin nhắn sẽ được trả lời tự động.",
        inline=False
    )
    
    embed.add_field(
        name="🔍 Sử dụng prefix",
        value=(
            "Bạn có thể sử dụng các prefix sau để hỏi AI ở bất kỳ kênh nào:\n"
            "• `hỏi [câu hỏi]`\n"
            "• `ai: [câu hỏi]`\n"
            "• `ai [câu hỏi]`\n"
            "• `chat: [câu hỏi]`"
        ),
        inline=False
    )
    
    embed.add_field(
        name="👋 Mention bot",
        value=f"Mention <@{self.bot.user.id}> và đặt câu hỏi của bạn.",
        inline=False
    )
    
    embed.add_field(
        name="⚡ Slash Commands",
        value=(
            "• `/ai [câu hỏi]` - Hỏi AI một câu hỏi\n"
            "• `/list_channels` - Xem danh sách kênh AI\n"
            "• `/add_channel` - Thêm kênh vào danh sách AI (Admin)\n"
            "• `/remove_channel` - Xóa kênh khỏi danh sách AI (Admin)"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🛠️ Lệnh thông thường",
        value=(
            "• `.add_channel [kênh]` - Thêm kênh vào danh sách AI\n"
            "• `.remove_channel [kênh]` - Xóa kênh khỏi danh sách AI\n"
            "• `.list_channels` - Xem danh sách kênh AI"
        ),
        inline=False
    )
    
    embed.set_footer(text="mèo kon")
    
    await ctx.reply(embed=embed)

# Also, in your main help command, add a section about AI
# For example, in your general help command:
@commands.command(name="help")
async def help_command(self, ctx, command=None):
    if command == "ai":
        await self.help_ai(ctx)
        return
        
    # ... rest of your help command ...
    
    # Add a section about AI in your general help
    embed.add_field(
        name="🤖 AI Commands",
        value="Use `.help ai` for detailed information about AI commands.",
        inline=False
    )
    
    # ... rest of your help command ...