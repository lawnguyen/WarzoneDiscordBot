import asyncio
import time
import discord

class DiscordBot(discord.Client):

    def __init__(self, processor, mode):
        super().__init__()
        self.processor = processor
        self.mode = mode

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
            cash_total = self.processor.get_cash_total(i)
            await main_channel.send("Total cash is {}".format(cash_total), tts = True, delete_after = 0)

            if (self.mode == "4"):
                input("Press Enter to continue...")
            

    
