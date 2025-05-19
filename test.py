import discord
import os # default module
from dotenv import load_dotenv
import random

load_dotenv() # load all the variables from the env file
bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.command()
# pycord will figure out the types for you
async def add(ctx, first: discord.Option(int), second: discord.Option(int)):
    # you can use them as they were actual integers
    sum = first + second
    await ctx.respond(f"The sum of {first} and {second} is {sum}.")

class MyView(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
    @discord.ui.button(label="Click me!", style=discord.ButtonStyle.primary, emoji="😎") # Create a button with the label "😎 Click me!" with color Blurple
    async def button_callback(self, button, interaction):
        await interaction.response.send_message("You clicked the button!") # Send a message when the button is clicked

    @discord.ui.button(label="Click me!", style=discord.ButtonStyle.danger, emoji="😎") # Create a button with the label "😎 Click me!" with color Blurple
    async def button_callback(self, button, interaction):
        await interaction.response.send_message("You clicked the button!") # Send a message when the button is clicked




@bot.slash_command() # Create a slash command
async def button(ctx):
    await ctx.respond("This is a button!", view=MyView())

bot.run(os.getenv('disPoken')) # run the bot with the token