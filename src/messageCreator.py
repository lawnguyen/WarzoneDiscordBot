import constants
import math

__all__ = ["create"]

def create(cash_total, buy_back_count, time_elapsed):
    if (cash_total < constants.BUY_BACK_COST or
        (cash_total < constants.LOADOUT_COST and buy_back_count == 0)):

        # To avoid sending too many un-useful messages, let's only send a message
        # if we can afford a loadout or if we need to buy a player back
        return None
    
    message = "Total cash is ${}".format(cash_total)

    if (cash_total >= constants.LOADOUT_COST):
        message += ", you can buy a loadout drop"
        if (buy_back_count >= 1):
            message += " or"

    if (buy_back_count >= 1 and cash_total >= constants.BUY_BACK_COST):
        buy_back_amount = math.floor(cash_total / constants.BUY_BACK_COST)
        message += ", you can buy back {} of your teammates".format(
            min(buy_back_amount, buy_back_count))

    # TODO: Created in-game messages based on time_elapsed

    return message