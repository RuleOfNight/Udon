import discord
from discord.ext import commands
from config import disPoken
from chat import init_gemini
from commands.voice import setup as voice_setup
from events import on_ready, on_message

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.dm_messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Setup modules
genai_configured, model = init_gemini()
voice_setup(bot)
on_ready.setup(bot, model)
on_message.setup(bot, model, genai_configured)

if __name__ == "__main__":
    bot.run(disPoken)
