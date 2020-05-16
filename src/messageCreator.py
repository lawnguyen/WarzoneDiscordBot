import constants
import math

__all__ = ["create"]

def create(cash_total, buy_back_count):
    if (cash_total == 0):
        return None
    
    message = "Total cash is ${}".format(cash_total)

    if (cash_total >= constants.LOADOUT_COST):
        message += ", you can buy a loadout drop"
        if (buy_back_count >= 1):
            message += " or"

    if (buy_back_count >= 1):
        buy_back_amount = math.floor(cash_total / constants.BUY_BACK_COST)
        message += ", you can buy back {} of your teammates".format(buy_back_amount)

    return message