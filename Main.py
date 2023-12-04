import random
import discord
import asyncio
import datetime

from discord.ext import commands

TOKEN = '' #Cất phòng khi bay token con bot

client = discord.Client()


@client.event
async def on_message(message):
    empty_array = []
    modmail_channel = discord.utils.get(client.get_all_channels(), name="⌈💬⌋chat-tào-lao")

    if message.author == client.user:
        return
    if str(message.channel.type) == "private":
        if message.attachments != empty_array:
            files = message.attachments
            await modmail_channel.send("From ["+ message.author.display_name + "]")

            for file in files:
                await modmail_channel.send(file.url)
        else:
            await modmail_channel.send(message.content)

    elif str(message.channel) == "⌈💬⌋chat-tào-lao" and message.content.startswith("<"):
        member_object = message.mentions[0]
        if message.attachments != empty_array:
            files = message.attachments
            await member_object.send("From ["+ message.author.display_name + "]")

            for file in files:
                await member_object.send(file.url)
        else:
            index = message.content.index(" ")
            string = message.content
            mod_message = string[index:]
            await member_object.send("From [" + message.author.display_name + "]" + mod_message)


client.run('OTExNTE1MjA5MTU4NDk2MjY3.YZigsA.Zwnf8m-MkPeYMha6cQj9i78VnFM')



def time():
    Time=datetime.datetime.now().strftime("%I:%M:%p")



        

@client.event
async def on_ready():
    print(' {0.user} giáng lâm'.format(client))

@client.event 
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    Time = datetime.datetime.now().strftime("%I:%M:%p")
    print(f'{username}: {user_message} ({channel})')



    if message.channel.name == '⁅💬⁆chat-tào-lao':
        if user_message.lower() == 'kéo':
            await message.channel.send(f'🔨')
            return
        if user_message.lower() == 'búa':
            await message.channel.send(f'🗑')
            return
        if user_message.lower() == 'bao':
            await message.channel.send(f'✂')
            

       
    elif user_message.lower() == ',do độ đẹp trai':
           response = f'Độ đẹp trai của bạn là {random.randrange(100)}/100 điểm'
           await message.channel.send(response)


        

    elif user_message.lower() == ',công thức after/before':
            await message.channel.send(f'After + S + had-pII,S + Vqk')
            await message.channel.send(f'Before + S + Vqk,S + had + pII')
            return
    elif user_message.lower() == ',v-ing':
            await message.channel.send(f'like,enjoy,look forward to,finish,be fond of,hate,dislike,spend,suggest,...')
            return
    elif user_message.lower() == ',v-ed':
            await message.channel.send(f'want,decide,ask,would you like,invite,it takes sb,use to,...')
            return
        



client.run(TOKEN)


