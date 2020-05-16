import asyncio
import time
import discord
import messageCreator

class DiscordBot(discord.Client):

    def __init__(self, processor, mode):
        super().__init__()
        self._processor = processor
        self._mode = mode
        self._message_frequency = 60    # in seconds
        self._target_channel = "general"

    async def on_ready(self):
        print("\nDiscord bot is ready\n")

        # TODO: Add game-has-started detection
        await self._main_loop()

    async def _main_loop(self):
        main_channel = None
        channels = self.get_all_channels()
        for channel in channels:
            if (channel.name == self._target_channel):
                main_channel = channel
        
        i = 0
        while (1):
            await asyncio.sleep(self._message_frequency)
            i += 1

            cash_total = self._processor.get_cash_total(i)
            buy_back_count = self._processor.buy_back_count
            message = messageCreator.create(cash_total, buy_back_count)

            if (message):
                await main_channel.send(message, tts = True, delete_after = 0)

            if (self._mode == "4"):
                input("Press Enter to continue...")
    
