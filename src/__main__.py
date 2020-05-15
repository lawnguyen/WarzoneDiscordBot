import sys
import time

import config
import menu
from discordBot import DiscordBot
from processor import Processor

if __name__ == "__main__": 
    if (len(sys.argv) == 2):
        display_number = int(sys.argv[1])
    else:
        display_number = int(input("Display number that modern warfare is running on (e.g. 2): "))

    menu.show_menu()
    mode = menu.get_choice()
    processor = Processor(display_number, mode)
    bot_client = DiscordBot(processor, mode)
    bot_client.run(config.DISCORD_BOT_TOKEN)
