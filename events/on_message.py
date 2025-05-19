import asyncio
import discord
from config import MODMAIL_CHANNEL_NAME
from prompts import load_prompt

def setup(bot, model, genai_configured):
    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return


        # Modmail
        if isinstance(message.channel, discord.DMChannel):
            modmail_channel = discord.utils.get(bot.get_all_channels(), name=MODMAIL_CHANNEL_NAME)
            if modmail_channel:
                embed = discord.Embed(description=message.content, timestamp=message.created_at, color=discord.Color.blue())
                embed.set_author(name=message.author.name, icon_url=message.author.display_avatar.url)
                embed.set_footer(text="Mod Mail")
                await modmail_channel.send(embed=embed)
                await message.add_reaction("✅")
            return

        # Mention Bot
        if bot.user in message.mentions and genai_configured and model:
            user_input = message.content.replace(f'<@!{bot.user.id}>', '').replace(f'<@{bot.user.id}>', '').strip()
            if not user_input:
                return
            full_prompt = f"{load_prompt()}\n\nNgười dùng: {user_input}\nUdon:"
            async with message.channel.typing():
                try:
                    response = await model.generate_content_async(full_prompt)
                    if response and response.text:
                        await message.reply(response.text.strip(), mention_author=False)
                    else:
                        await message.reply("Tớ nghĩ hơi chậm, nói lại phát 😵", mention_author=False)
                except Exception as e:
                    await message.reply(f"Ối, lỗi `{type(e).__name__}` xảy ra rồi!", mention_author=False)

