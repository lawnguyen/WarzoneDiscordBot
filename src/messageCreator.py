import constants
import math

__all__ = ["create"]

def create(cash_total, buy_back_count):
    if (cash_total < 4000):
        # For now, don't send a message unless we have >= $4000 since any
        # lower of a total is not very useful to the entire team
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

    return message