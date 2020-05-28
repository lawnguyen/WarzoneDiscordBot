import sys
import time
import logging
import discord

import config
import menu
from discordBot import DiscordBot
from processor import Processor

if __name__ == "__main__": 
    # Set up logging of discord module
    logger = logging.getLogger("discord")
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='discordbot.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

    if (len(sys.argv) == 2):
        display_number = int(sys.argv[1])
    else:
        display_number = int(
            input("Display number that modern warfare is running on (e.g. 2): "))

    menu.show_menu()
    mode = menu.get_choice()
    processor = Processor(display_number, mode)
    bot_client = DiscordBot(processor, mode)
    bot_client.loop.create_task(bot_client.main_loop_background_task())
    bot_client.run(config.DISCORD_BOT_TOKEN)
