def setup(bot, model):
    @bot.event
    async def on_ready():
        print(f"Bot {bot.user} đã online!")
        if model:
            print(f"Model: {model.model_name}")
