import asyncio
import time
import discord
import math
import constants

class DiscordBot(discord.Client):

    def __init__(self, processor, mode):
        super().__init__()
        self._processor = processor
        self._mode = mode

    async def on_ready(self):
        print("\nDiscord bot is ready\n")

        # TODO: Add game-has-started detection, for now just wait 10 seconds until executing
        await self._main_loop()

    async def _main_loop(self):
        main_channel = None
        channels = self.get_all_channels()
        for channel in channels:
            if (channel.name == "general"):
                main_channel = channel
        
        i = 0
        while (1):
            await asyncio.sleep(10)
            i += 1

            cash_total = self._processor.get_cash_total(i)
            buy_back_count = self._processor.buy_back_count
            message = self._create_message(cash_total, buy_back_count)

            if (message):
                await main_channel.send(message, tts = True, delete_after = 0)

            if (self._mode == "4"):
                input("Press Enter to continue...")
            
    def _create_message(self, cash_total, buy_back_count):
        if (cash_total == 0):
            return None
        
        message = "Total cash is {}".format(cash_total)

        if (cash_total >= constants.LOADOUT_COST):
            message += ", you can buy a loadout drop"
            if (buy_back_count >= 1):
                message += " or"

        if (buy_back_count >= 1):
            buy_back_amount = math.floor(cash_total / constants.BUY_BACK_COST)
            message += ", you can buy back {} of your teammates".format(buy_back_amount)

        return message
    
