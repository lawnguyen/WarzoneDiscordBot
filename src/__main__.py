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
    bot_client = DiscordBot()
    bot_client.run(config.DISCORD_BOT_TOKEN)
    
    # TODO: Add game-has-started detection, for now just wait 10 seconds until executing
    time.sleep(10)

    i = 0
    while (1):
        i += 1
        cash_total = processor.get_cash_total(i)
        if (mode == "4"):
            input("Press Enter to continue...")
        time.sleep(10)
