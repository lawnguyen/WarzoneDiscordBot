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

        i = 0
        while (1):
            await asyncio.sleep(10)
            i += 1
            cash_total = self.processor.get_cash_total(i)

            if (self.mode == "4"):
                input("Press Enter to continue...")
            

    
