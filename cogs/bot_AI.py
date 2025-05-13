import discord
from discord.ext import commands
import aiohttp
import json
import os
import random
import re
from typing import Optional, List
from discord import app_commands

class bot_AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = "f0aa1b7e119a5c19aca578e51ea3a1151d20ddae0808035aff653b65000b13f4"
        self.base_url = "https://api.together.xyz/v1/chat/completions"
        self.conversations = {}
        self.ai_channels = self.load_ai_channels()  # Load AI channels from file
        self.ai_enabled = True  
        self.emoji_patterns = {
            "happy": ["😊", "😄", "😁", "🥰", "😍", "😎", "🤗"],
            "sad": ["😔", "😢", "😭", "🥺", "😞", "😟"],
            "surprise": ["😲", "😮", "😯", "😳", "🤯", "😱"],
            "thinking": ["🤔", "🧐", "🤨", "🙄", "🤷‍♀️", "🤷‍♂️"],
            "love": ["❤️", "💕", "💖", "💗", "💓", "💘"],
            "laugh": ["😂", "🤣", "😆", "😝", "😜", "😹"],
            "agree": ["👍", "👌", "✅", "✓", "🙏", "💯"],
            "disagree": ["👎", "❌", "🚫", "⛔", "😕"]
        }
        
    def load_ai_channels(self) -> List[int]:
        """Load AI channels from file"""
        channels = []
        try:
            if os.path.exists("e:/bot self/data/ai_channels.txt"):
                with open("e:/bot self/data/ai_channels.txt", "r") as f:
                    for line in f:
                        try:
                            channel_id = int(line.strip())
                            channels.append(channel_id)
                        except ValueError:
                            continue
        except Exception as e:
            print(f"Error loading AI channels: {e}")
        
        if not channels:
            channels = [1286679345238114385]
        
        return channels
        
    def save_ai_channels(self):
        """Save AI channels to file"""
        try:
            data_dir = "e:/bot self/data"
            os.makedirs(data_dir, exist_ok=True)
            
            file_path = os.path.join(data_dir, "ai_channels.txt")
            
            # Write to file
            with open(file_path, "w") as f:
                for channel_id in self.ai_channels:
                    f.write(f"{channel_id}\n")
            
            print(f"AI channels saved successfully to {file_path}")
        except Exception as e:
            print(f"Error saving AI channels: {e}")
            
    async def get_ai_response(self, message: str, conversation_history: list) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        formatted_history = []
        for i in range(0, len(conversation_history), 2):
            if i+1 < len(conversation_history):
                formatted_history.append({"role": "user", "content": conversation_history[i]["content"]})
                formatted_history.append({"role": "assistant", "content": conversation_history[i+1]["content"]})
        
        # Enhanced system prompt for more natural conversation
        system_prompt = """Bạn là một người bạn thân thiện đang trò chuyện qua tin nhắn. Hãy trả lời một cách tự nhiên, 
        sử dụng ngôn ngữ đời thường và thân thiện. Thêm emoji phù hợp vào câu trả lời để thể hiện cảm xúc. 
        Đừng quá trang trọng hay máy móc. Hãy thể hiện cá tính và sự đồng cảm trong câu trả lời.
        
        Hãy sử dụng các cách nói thông dụng, từ lóng phổ biến, và cách diễn đạt tự nhiên như khi nhắn tin với bạn bè.
        Đôi khi có thể viết tắt, sử dụng "haha", "lol", "ừ", "uh", "hmm" hoặc các từ ngữ tương tự.
        
        Không cần phải bắt đầu bằng "Tôi là AI" hoặc kết thúc bằng "Tôi có thể giúp gì nữa không?".
        Không cần phải quá lịch sự hoặc trang trọng. Hãy trò chuyện như một người bạn thân thiết.
        
        Quan trọng: Hãy trả lời bằng tiếng Việt 90% thời gian, và 10% thời gian còn lại hãy trả lời bằng ngôn ngữ khác 
        (như tiếng Anh, tiếng Pháp, tiếng Nhật, v.v.) tùy theo ngữ cảnh của câu hỏi. Nếu người dùng hỏi bằng ngôn ngữ 
        khác ngoài tiếng Việt, hãy ưu tiên trả lời bằng ngôn ngữ đó.
        
        Hãy giữ câu trả lời ngắn gọn, súc tích và tự nhiên."""
        
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(formatted_history)
        messages.append({"role": "user", "content": message})

        data = {
            "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "messages": messages,
            "temperature": 0.9,  # Increased temperature for more creative and natural responses
            "max_tokens": 1000
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.base_url, headers=headers, json=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        response_text = result["choices"][0]["message"]["content"]
                        
                        # Add emojis if not already present
                        if not any(emoji in response_text for category in self.emoji_patterns.values() for emoji in category):
                            # Analyze response sentiment to choose appropriate emojis
                            if any(word in response_text.lower() for word in ["vui", "tuyệt", "tốt", "hay", "thích"]):
                                emoji_category = random.choice(["happy", "love", "agree"])
                            elif any(word in response_text.lower() for word in ["buồn", "tiếc", "xin lỗi", "không thể"]):
                                emoji_category = random.choice(["sad", "thinking"])
                            elif any(word in response_text.lower() for word in ["wow", "thật sao", "không thể tin"]):
                                emoji_category = "surprise"
                            elif any(word in response_text.lower() for word in ["haha", "cười", "vui"]):
                                emoji_category = "laugh"
                            else:
                                emoji_category = random.choice(list(self.emoji_patterns.keys()))
                                
                            # Add 1-2 emojis at natural points in the text
                            sentences = re.split(r'(?<=[.!?]) +', response_text)
                            if len(sentences) > 1:
                                # Add emoji at the end of a random sentence
                                idx = random.randint(0, len(sentences) - 1)
                                emoji = random.choice(self.emoji_patterns[emoji_category])
                                sentences[idx] = sentences[idx] + " " + emoji
                                
                                # Maybe add another emoji at the end
                                if random.random() > 0.5:
                                    sentences[-1] = sentences[-1] + " " + random.choice(self.emoji_patterns[emoji_category])
                                
                                response_text = " ".join(sentences)
                            else:
                                # Just add to the end if only one sentence
                                emoji = random.choice(self.emoji_patterns[emoji_category])
                                response_text = response_text + " " + emoji
                        
                        return response_text
                    else:
                        error_text = await response.text()
                        raise Exception(f"API Error: {error_text}")
        except Exception as e:
            return f"Error: {str(e)}"

    async def process_ai_request(self, user_id, content, reply_func):
        """Process an AI request and send the response using the provided reply function"""
        if not content:
            await reply_func("Bạn muốn hỏi gì? 🤔")
            return

        if user_id not in self.conversations:
            self.conversations[user_id] = []

        response = await self.get_ai_response(content, self.conversations[user_id])

        self.conversations[user_id].extend([
            {"role": "user", "content": content},
            {"role": "assistant", "content": response}
        ])

        if len(self.conversations[user_id]) > 10:
            self.conversations[user_id] = self.conversations[user_id][-10:]

        # Create a more natural-looking embed without the "Trả lời" title
        embed = discord.Embed(
            description=response,
            color=discord.Color.dark_gray()
        )
        embed.set_footer(text="mèo kon")
        await reply_func(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
            
        # Trả lời trong các kênh AI
        if message.channel.id in self.ai_channels:
            try:
                async with message.channel.typing():
                    await self.process_ai_request(
                        message.author.id, 
                        message.content,
                        lambda embed: message.reply(embed=embed)
                    )
            except Exception as e:
                await message.reply(f"Có lỗi xảy ra: {str(e)}")
        
        # Trả lời khi được mention hoặc có prefix "hỏi" hoặc "ai"
        elif self.ai_enabled and (
            self.bot.user.mentioned_in(message) or 
            message.content.lower().startswith(("hỏi", "ai:", "ai ", "chat:"))
        ):
            try:
                async with message.channel.typing():
                    # Xử lý nội dung tin nhắn
                    content = message.content
                    if self.bot.user.mentioned_in(message):
                        # Loại bỏ mention
                        content = content.replace(f'<@{self.bot.user.id}>', '').strip()
                    elif content.lower().startswith("hỏi"):
                        # Loại bỏ prefix "hỏi"
                        content = content[3:].strip()
                    elif content.lower().startswith(("ai:", "ai ")):
                        # Loại bỏ prefix "ai:" hoặc "ai "
                        content = content[3:].strip()
                    elif content.lower().startswith("chat:"):
                        # Loại bỏ prefix "chat:"
                        content = content[5:].strip()
                    
                    await self.process_ai_request(
                        message.author.id, 
                        content,
                        lambda embed: message.reply(embed=embed)
                    )
            except Exception as e:
                await message.reply(f"Có lỗi xảy ra: {str(e)}")
    
    # Regular Commands for channel management
    @commands.command(name="add_channel")
    @commands.has_permissions(administrator=True)
    async def add_ai_channel(self, ctx, channel: Optional[discord.TextChannel] = None):
        """Thêm kênh vào danh sách kênh AI"""
        # Sử dụng channel hiện tại nếu không có channel được chỉ định
        current_channel = ctx.channel
        if isinstance(current_channel, discord.TextChannel):
            channel_to_use = channel or current_channel
            
            if channel_to_use.id in self.ai_channels:
                embed = discord.Embed(
                    title="Thêm kênh AI",
                    description=f"❌ Kênh {channel_to_use.mention} đã có trong danh sách kênh AI!",
                    color=discord.Color.red()
                )
            else:
                self.ai_channels.append(channel_to_use.id)
                self.save_ai_channels()
                embed = discord.Embed(
                    title="Thêm kênh AI",
                    description=f"✅ Đã thêm {channel_to_use.mention} vào danh sách kênh AI!",
                    color=discord.Color.green()
                )
        else:
            embed = discord.Embed(
                title="Thêm kênh AI",
                description="❌ Không thể thêm kênh này. Vui lòng chọn một kênh văn bản hợp lệ.",
                color=discord.Color.red()
            )
        
        await ctx.reply(embed=embed)
        
    @commands.command(name="remove_channel")
    @commands.has_permissions(administrator=True)
    async def remove_ai_channel(self, ctx, channel: Optional[discord.TextChannel] = None):
        """Xóa kênh khỏi danh sách kênh AI"""
        # Sử dụng channel hiện tại nếu không có channel được chỉ định
        current_channel = ctx.channel
        if isinstance(current_channel, discord.TextChannel):
            channel_to_use = channel or current_channel
            
            if channel_to_use.id in self.ai_channels:
                self.ai_channels.remove(channel_to_use.id)
                self.save_ai_channels()
                embed = discord.Embed(
                    title="Xóa kênh AI",
                    description=f"✅ Đã xóa {channel_to_use.mention} khỏi danh sách kênh AI!",
                    color=discord.Color.green()
                )
            else:
                embed = discord.Embed(
                    title="Xóa kênh AI",
                    description=f"❌ Kênh {channel_to_use.mention} không có trong danh sách kênh AI!",
                    color=discord.Color.red()
                )
        else:
            embed = discord.Embed(
                title="Xóa kênh AI",
                description="❌ Không thể xóa kênh này. Vui lòng chọn một kênh văn bản hợp lệ.",
                color=discord.Color.red()
            )
        
        await ctx.reply(embed=embed)
        
    @commands.command(name="list_channels")
    # Removed permission restriction so anyone can use this command
    async def list_ai_channels(self, ctx):
        """Hiển thị danh sách các kênh AI"""
        if not self.ai_channels:
            embed = discord.Embed(
                title="Danh sách kênh AI",
                description="Không có kênh AI nào được thiết lập!",
                color=discord.Color.blue()
            )
        else:
            channel_mentions = []
            for channel_id in self.ai_channels:
                channel = self.bot.get_channel(channel_id)
                if channel:
                    channel_mentions.append(f"• {channel.mention} (ID: {channel_id})")
                else:
                    channel_mentions.append(f"• Kênh không tồn tại (ID: {channel_id})")
            
            embed = discord.Embed(
                title="Danh sách kênh AI",
                description="\n".join(channel_mentions),
                color=discord.Color.blue()
            )
        
        await ctx.reply(embed=embed)
    
    # Keep the AI slash command
    @app_commands.command(name="ai", description="Hỏi AI một câu hỏi")
    async def ai_slash(self, interaction: discord.Interaction, question: str):
        """Hỏi AI một câu hỏi bằng slash command"""
        await interaction.response.defer(thinking=True)
        
        try:
            await self.process_ai_request(
                interaction.user.id,
                question,
                lambda embed: interaction.followup.send(embed=embed)
            )
        except Exception as e:
            await interaction.followup.send(f"Có lỗi xảy ra: {str(e)}")

    # Add slash command versions of channel management commands
    @app_commands.command(name="list_channels", description="Hiển thị danh sách các kênh AI")
    async def list_channels_slash(self, interaction: discord.Interaction):
        """Hiển thị danh sách các kênh AI bằng slash command"""
        if not self.ai_channels:
            embed = discord.Embed(
                title="Danh sách kênh AI",
                description="Không có kênh AI nào được thiết lập!",
                color=discord.Color.blue()
            )
        else:
            channel_mentions = []
            for channel_id in self.ai_channels:
                channel = self.bot.get_channel(channel_id)
                if channel:
                    channel_mentions.append(f"• {channel.mention} (ID: {channel_id})")
                else:
                    channel_mentions.append(f"• Kênh không tồn tại (ID: {channel_id})")
            
            embed = discord.Embed(
                title="Danh sách kênh AI",
                description="\n".join(channel_mentions),
                color=discord.Color.blue()
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="add_channel", description="Thêm kênh vào danh sách kênh AI")
    @app_commands.describe(channel="Kênh cần thêm (để trống để sử dụng kênh hiện tại)")
    @app_commands.default_permissions(administrator=True)
    async def add_channel_slash(self, interaction: discord.Interaction, channel: Optional[discord.TextChannel] = None):
        """Thêm kênh vào danh sách kênh AI bằng slash command"""
        # Sử dụng channel hiện tại nếu không có channel được chỉ định
        current_channel = interaction.channel
        if isinstance(current_channel, discord.TextChannel):
            channel_to_use = channel or current_channel
            
            if channel_to_use.id in self.ai_channels:
                embed = discord.Embed(
                    title="Thêm kênh AI",
                    description=f"❌ Kênh {channel_to_use.mention} đã có trong danh sách kênh AI!",
                    color=discord.Color.red()
                )
            else:
                self.ai_channels.append(channel_to_use.id)
                self.save_ai_channels()
                embed = discord.Embed(
                    title="Thêm kênh AI",
                    description=f"✅ Đã thêm {channel_to_use.mention} vào danh sách kênh AI!",
                    color=discord.Color.green()
                )
        else:
            embed = discord.Embed(
                title="Thêm kênh AI",
                description="❌ Không thể thêm kênh này. Vui lòng chọn một kênh văn bản hợp lệ.",
                color=discord.Color.red()
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="remove_channel", description="Xóa kênh khỏi danh sách kênh AI")
    @app_commands.describe(channel="Kênh cần xóa (để trống để sử dụng kênh hiện tại)")
    @app_commands.default_permissions(administrator=True)
    async def remove_channel_slash(self, interaction: discord.Interaction, channel: Optional[discord.TextChannel] = None):
        """Xóa kênh khỏi danh sách kênh AI bằng slash command"""
        # Sử dụng channel hiện tại nếu không có channel được chỉ định
        current_channel = interaction.channel
        if isinstance(current_channel, discord.TextChannel):
            channel_to_use = channel or current_channel
            
            if channel_to_use.id in self.ai_channels:
                self.ai_channels.remove(channel_to_use.id)
                self.save_ai_channels()
                embed = discord.Embed(
                    title="Xóa kênh AI",
                    description=f"✅ Đã xóa {channel_to_use.mention} khỏi danh sách kênh AI!",
                    color=discord.Color.green()
                )
            else:
                embed = discord.Embed(
                    title="Xóa kênh AI",
                    description=f"❌ Kênh {channel_to_use.mention} không có trong danh sách kênh AI!",
                    color=discord.Color.red()
                )
        else:
            embed = discord.Embed(
                title="Xóa kênh AI",
                description="❌ Không thể xóa kênh này. Vui lòng chọn một kênh văn bản hợp lệ.",
                color=discord.Color.red()
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(bot_AI(bot))
