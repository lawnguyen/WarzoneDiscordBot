import asyncio
import time
import discord
import messageCreator
from timer import Timer

class DiscordBot(discord.Client):

    def __init__(self, processor, mode):
        super().__init__()
        self._processor = processor
        self._mode = mode
        self._message_frequency = 60    # in seconds
        self._target_channel = "general"
        self._game_timer = Timer()
        self._message_timer = Timer()

    async def on_ready(self):
        print("\nDiscord bot is ready\n")

        while (1):
            if (self._processor.is_game_started()):
                break
        print("Game started\n")
        self._game_timer.start_timer()
        await self._main_loop()

        # TODO: Listen for command to restart when starting a new game

    async def _main_loop(self):
        main_channel = None
        channels = self.get_all_channels()
        for channel in channels:
            if (channel.name == self._target_channel):
                main_channel = channel
        
        i = 0
        while (1):
            i += 1

            cash_total = self._processor.get_cash_total(i)
            buy_back_count = self._processor.buy_back_count
            message = messageCreator.create(
                cash_total, buy_back_count, self._game_timer.get_time_elapsed)

            if (message):
                await main_channel.send(message, tts = True, delete_after = 0)

            if (self._mode == "4"):
                input("Press Enter to continue...")

    def should_send_message(self):
        # TODO: Add logic for message frequency
    
