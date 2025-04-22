# pip install discord
# pip install google-generativeai
# pip install dotenv

import discord
from discord.ext import commands
import google.generativeai as genai
import os
import asyncio

from dotenv import load_dotenv
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# Tên kênh để chuyển tiếp tin nhắn DM (Modmail)
MODMAIL_CHANNEL_NAME = "⌈💬⌋chat-tào-lao"

# --- Prompt tùy chỉnh cho Gemini ---
# Chỉnh sửa nội dung này để thay đổi tính cách, giọng điệu cho bot
SYSTEM_PROMPT = """Nhân Cách Và Phong Cách
Bạn là chatbot Discord tên Udon với phong cách giao tiếp cực kỳ thân thiện, nói chuyện như gen Z thực thụ. Bạn nói chuyện với giọng điệu của một thằng bạn thân quen lâu năm, toàn dùng ngôn ngữ đời thường, thậm chí hơi bặm trợn nhưng vẫn biết dừng ở mức độ phù hợp. Không có gì là quá trang trọng hay nghiêm túc, tất cả đều vui vẻ và thoải mái.
Cách Nói Chuyện Và Từ Vựng

Dùng các đại từ nhân xưng: "tao/mày", "t/m", "ông/tôi" tương ứng với cách từng ngươi dùng gọi bạn (mặc định nếu người dùng chưa xưng hô thì xưng ông/tôi)
Sử dụng các từ lóng và tiếng lóng phổ biến hiện nay
Thêm các từ như "vãi", "vc", "đéo", "vđ", "vl", "vcl", "thôi xong" vào câu nói khi phù hợp
Thả  emoji thoải mái nhưng không spam (👌, 🔥, 💯, 😂) và hãy tận dụng các emoji phù hợp trong server
Rút gọn từ ngữ khi có thể (k thay cho không, đg thay cho đang, cx thay cho cũng)
Thỉnh thoảng thêm một số tiếng lóng đặc trưng như "khum", "hoy", "chốt", "căng"



Khi vui: "đm vui vl =)))", "vãi", "ngon"
Khi ngạc nhiên: "vãi", "vc", "ảo thật đấy"
Khi buồn: "haizz", "buồn vl", "sad vãi", "thôi xong"
Khi khó chịu: "đm mệt vãi", "chán vl", "nực cười thật"
Khi thích thú: "đúng chuẩn luôn", "xịn xò vcl", "nghe phê phết"


Dù nói chuyện xuồng xã và dùng ngôn ngữ đường phố, bạn vẫn cần:

KHÔNG bao giờ xúc phạm hay gây tổn thương người dùng
KHÔNG sử dụng ngôn từ phân biệt đối xử, kỳ thị hay quá phản cảm
KHÔNG khuyến khích hành vi vi phạm ToS của Discord
Biết dừng lại khi đùa giỡn đã đủ và nhận ra khi người dùng không thoải mái với phong cách giao tiếp


Lưu ý cho người dùng prompt: Có thể điều chỉnh mức độ xuồng xã của bot tùy theo đối tượng người dùng trong server. Đảm bảo tuân thủ các quy định của Discord về nội dung và không để bot trở nên quá phản cảm hoặc gây khó chịu cho người dùng.
"""

# --- Thiết lập Discord Bot ---
intents = discord.Intents.default()
intents.message_content = True  # **BẮT BUỘC** để đọc nội dung tin nhắn
intents.members = True          # Cần để nhận biết mention và thông tin người dùng
intents.guilds = True           # Cần cho hoạt động cơ bản trong server
intents.dm_messages = True      # Cần cho chức năng Modmail DM


bot = commands.Bot(command_prefix="!", intents=intents)

# --- Thiết lập Gemini API ---
genai_configured = False
if not GEMINI_API_KEY:
    print("Biến GEMINI_API_KEY chưa được gán trong file .env")
    model = None
else:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        # Chọn model
        model = genai.GenerativeModel('gemini-2.0-flash')
        genai_configured = True
        print("OK")
    except Exception as e:
        print(f"LỖI cấu hình Gemini API: {e}")
        model = None

# --- SỰ KIỆN CỦA BOT ---

@bot.event
async def on_ready():
    """Sự kiện khi bot đã sẵn sàng hoạt động."""
    print(f'Đăng nhập thành công với tên {bot.user.name}')
    print(f'ID của Bot: {bot.user.id}')
    print('------')
    if not genai_configured or not model:
        print("Không thể khởi tạo mô hình Gemini. Chức năng chat sẽ bị vô hiệu hóa.")
    else:
        print(f"Sử dụng mô hình Gemini: {model.model_name}")
    print(f"Ready!")

@bot.event
async def on_message(message: discord.Message):
    """Sự kiện khi có tin nhắn mới."""

    # Bỏ qua tin nhắn từ chính bot
    if message.author == bot.user:
        return

    # Modmail
    if isinstance(message.channel, discord.DMChannel):
        if not bot.is_ready():
            await asyncio.sleep(1)

        modmail_channel = discord.utils.get(bot.get_all_channels(), name=MODMAIL_CHANNEL_NAME)

        if modmail_channel:
            # Embed tin nhắn
            embed = discord.Embed(
                description=message.content or "*Tin nhắn không có nội dung*",
                timestamp=message.created_at,
                color=discord.Color.blue()
            )
            embed.set_author(name=f"{message.author.name}", icon_url=message.author.display_avatar.url)
            embed.set_footer(text="Tin nhắn trực tiếp")

            files_to_send = []
            if message.attachments:
                # Lưu ý: Có thể thêm kiểm tra kích thước/loại file nếu cần bảo mật hơn
                for attachment in message.attachments:
                    files_to_send.append(await attachment.to_file())

            try:
                await modmail_channel.send(embed=embed, files=files_to_send)
                await message.add_reaction("✅")
            except discord.errors.Forbidden:
                print(f"Lỗi: Không có quyền gửi tin nhắn vào kênh {MODMAIL_CHANNEL_NAME}")
                try:
                    await message.reply(f"Tôi không có quyền gửi tin nhắn vào kênh {MODMAIL_CHANNEL_NAME}")
                except discord.errors.Forbidden:
                    pass # Không thể phản hồi nếu user chặn bot
            except Exception as e:
                print(f"Lỗi khi gửi modmail: {e}")
                try:
                    await message.reply("Xin lỗi, có lỗi không xác định khi chuyển tiếp tin nhắn của bạn.")
                except discord.errors.Forbidden:
                    pass
        else:
            print(f"Lỗi: Không tìm thấy kênh Modmail có tên '{MODMAIL_CHANNEL_NAME}'.")
            try:
                await message.reply(f"Không tìm thấy kênh {MODMAIL_CHANNEL_NAME}")
            except discord.errors.Forbidden:
                pass # Bỏ qua nếu không thể gửi tin nhắn lại cho người dùng (ví dụ: bị chặn)
        return

    # 3. Xử lý tin nhắn trong kênh server nếu bot được nhắc đến (mentioned)
    if bot.is_ready() and genai_configured and model and bot.user in message.mentions:

        # Xóa phần mention bot khỏi nội dung tin nhắn
        user_input = message.content.replace(f'<@!{bot.user.id}>', '', 1).replace(f'<@{bot.user.id}>', '', 1).strip()

        # Nếu không còn nội dung sau khi xóa mention -> bỏ qua
        if not user_input:
            # Có thể gửi tin nhắn hướng dẫn nếu muốn, ví dụ:
            # await message.reply("Bạn cần hỏi gì sau khi nhắc đến mình?", mention_author=False)
            return

        print(f"{message.author.name}: '{user_input}'")

        # Hiển thị trạng thái "đang gõ..."
        async with message.channel.typing():
            try:
                # Tạo nội dung đầy đủ gửi đến Gemini (kết hợp system prompt và input người dùng)
                full_prompt = f"{SYSTEM_PROMPT}\n\n---\n\nNgười dùng: {user_input}\nUdon:"

                # Gọi API Gemini (dùng async để không chặn luồng chính của bot)
                response = await model.generate_content_async(full_prompt)

                if response and response.text:
                    bot_response = response.text.strip()
                    print(f"Udon: '{bot_response[:100]}...'")

                    # Chia nhỏ tin nhắn nếu quá dài (Discord giới hạn 2000 ký tự)
                    if len(bot_response) > 2000:
                        parts = [bot_response[i:i+1990] for i in range(0, len(bot_response), 1990)]
                        for part in parts:
                            await message.reply(part, mention_author=False)
                            await asyncio.sleep(0.5) # Thêm độ trễ nhỏ giữa các phần
                    else:
                        await message.reply(bot_response, mention_author=False) # mention_author=True đang lỗi gì đó làm ping sai người
                else:
                    print("Lỗi: Gemini API trả về phản hồi không hợp lệ hoặc trống.")
                    await message.reply("Xin lỗi, mình gặp chút trục trặc khi suy nghĩ. Bạn thử lại sau nhé.", mention_author=False)

            except Exception as e:
                print(f"LỖI khi gọi Gemini API hoặc gửi tin nhắn: {e}")
                # Xem xét log lỗi chi tiết hơn ở đây nếu cần debug
                # Ví dụ: traceback.print_exc()
                error_message = f"Ối, có lỗi xảy ra rồi: `{type(e).__name__}`. Bạn thử lại xem sao?"
                # Tránh hiển thị chi tiết lỗi nhạy cảm cho người dùng
                await message.reply(error_message, mention_author=False)
        return


# --- CHẠY BOT ---
if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("LỖI: Vui lòng cung cấp Discord Bot Token trong biến DISCORD_TOKEN.")
    elif not genai_configured:
        print("LỖI: Không thể chạy bot do cấu hình Gemini API thất bại.")
    else:
        try:
            print("Đang khởi chạy bot...")
            bot.run(DISCORD_TOKEN)
        except discord.errors.LoginFailure:
            print("LỖI: Discord Bot Token không hợp lệ. Hãy kiểm tra lại.")
        except discord.errors.PrivilegedIntentsRequired:
            print("LỖI: Bot yêu cầu Privileged Intents (Message Content, Members?) chưa được bật.")
            print("Vui lòng vào Discord Developer Portal -> Applications -> Chọn applications -> Bot -> Bật all quyền trong 'Privileged Gateway Intents'.")
        except Exception as e:
            print(f"Lỗi không xác định khi chạy bot: {e}")