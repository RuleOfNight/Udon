from discord.ext import commands

def setup(bot):
    @bot.command()
    async def join(ctx):
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
            await ctx.send(f"Đã kết nối tới {ctx.author.voice.channel.name}, Udon on the mic!")
        else:
            await ctx.send("Không tìm thấy kênh voice có người dùng.")
