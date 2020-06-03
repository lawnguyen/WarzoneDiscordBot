import asyncio
import discord
import messageCreator
from timer import Timer

class DiscordBot(discord.Client):

    def __init__(self, processor, mode):
        super().__init__()
        self._processor = processor
        self._mode = mode
        
        self._message_frequency = 30    # in seconds
        self._target_guild = input("Discord guild: ")
        self._target_text_channel = input("Discord text channel (case sensitive): ")
        self._target_voice_channel = input("Discord voice channel (case sensitive): ")
        self.loadout_message_sent = False

        self._game_timer = Timer()
        self._message_timer = Timer()

    async def main_loop_background_task(self):
        await self.wait_until_ready()
        await self._init_discord_server_details()
        print("\nDiscord bot is ready\n")

        while (1):
            if (self._mode == "6" or self._processor.is_game_started()):
                break

        print("Match started\n")
        self._game_timer.restart_timer()
        self._message_timer.restart_timer()
        await self._main_loop()

    async def _main_loop(self):
        i = 0
        while (1):
            i += 1

            cash_total = self._processor.get_cash_total(i, 5)
            buy_back_count = self._processor.buy_back_count
            message = messageCreator.create(
                cash_total, 
                buy_back_count,
                self._game_timer.get_time_elapsed())

            if (self._should_send_message(message)):
                self._message_timer.restart_timer()
                message_sent = await self._main_text_channel.send(
                    message.content, tts = True)
                await message_sent.delete()

                if (message.messageType == "loadout_cash_prompt"):
                    # We realistically only want this message once
                    self.loadout_message_sent = True

            if (self._mode == "4"):
                input("Press Enter to continue...")

    async def _init_discord_server_details(self):
        self._main_text_channel = None
        self._main_voice_channel = None
        self._main_guild = None
        
        for guild in self.guilds:
            if (guild.name == self._target_guild):
                self._main_guild = guild
        for channel in self._main_guild.channels:
            if (self._main_text_channel and self._main_voice_channel):
                break

            if (not self._target_text_channel and channel.type.name == "text"):
                # Default to first channel
                self._main_text_channel = channel
            elif (channel.name == self._target_text_channel):
                self._main_text_channel = channel

            if (not self._target_voice_channel and channel.type.name == "voice"):
                # Default to first channel
                self._main_voice_channel = channel
                await channel.connect()
            elif (channel.name == self._target_voice_channel):
                self._main_voice_channel = channel
                await channel.connect()


    def _should_send_message(self, message):
        time_elapsed = self._message_timer.get_time_elapsed()

        if (message.messageType == "checkpoint"):
            if (self._mode == "6"):
                return False
            # always send checkpoint messages, regardless of frequency because 
            # are time-based and very useful
            return True
        
        if (message.messageType == "none" or
            time_elapsed < self._message_frequency or
            (self.loadout_message_sent == True and 
                message.messageType == "loadout_cash_prompt")):

            return False
        return True
