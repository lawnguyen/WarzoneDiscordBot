import asyncio
import discord
import messageCreator
from timer import Timer

class DiscordBot(discord.Client):

    def __init__(self, processor, mode):
        super().__init__()
        self._processor = processor
        self._mode = mode
        
        self._message_frequency = 20    # in seconds
        self._target_guild = "law bot testing"
        self._target_channel = "general"
        self.loadout_message_sent = False

        self._game_timer = Timer()
        self._message_timer = Timer()

    async def main_loop_background_task(self):
        await self.wait_until_ready()
        self._init_discord_server_details()
        print("\nDiscord bot is ready\n")

        while (1):
            if (self._processor.is_game_started()):
                break

        print("Match started\n")
        self._game_timer.restart_timer()
        self._message_timer.restart_timer()
        await self._main_loop()

    async def _main_loop(self):
        i = 0
        while (1):
            i += 1

            cash_total = self._processor.get_cash_total(i)
            buy_back_count = self._processor.buy_back_count
            message = messageCreator.create(
                cash_total, 
                buy_back_count,
                self._game_timer.get_time_elapsed())

            if (self._should_send_message(message)):
                self._message_timer.restart_timer()
                message_sent = await self._main_channel.send(message, tts = True)
                await message_sent.delete()

                if ("loadout" in message):
                    # We realistically only want this message once
                    self.loadout_message_sent = True

            if (self._mode == "4"):
                input("Press Enter to continue...")

    def _init_discord_server_details(self):
        self._main_channel = None
        self._main_guild = None
        
        for guild in self.guilds:
            if (guild.name == self._target_guild):
                self._main_guild = guild
        for channel in self._main_guild.channels:
            if (channel.name == self._target_channel):
                self._main_channel = channel

    def _should_send_message(self, message):
        if (not message or
            self._message_timer.get_time_elapsed() < self._message_frequency or
            (self.loadout_message_sent == True and "loadout" in message)):

            return False
        return True
