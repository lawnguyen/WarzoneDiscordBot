import constants
import math

__all__ = ["create"]

def create(cash_total, buy_back_count, time_elapsed):
    time_elapsed = int(time_elapsed)

    if (time_elapsed not in checkpoints and
        (cash_total < constants.BUY_BACK_COST or 
            (cash_total < constants.LOADOUT_COST and buy_back_count == 0))):

        # To avoid sending too many un-useful messages, let's only send a message
        # if we can:
        # 1. afford a loadout
        # 2. we need to buy a player back
        # 3. time has elapsed onto a checkpoint
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

    if (time_elapsed in checkpoints):
        message = checkpoints_messages_map[time_elapsed]

    return message

checkpoints_messages_map = {
    constants.GAME_START_CUT_SCENE: "match is starting",
    constants.CIRCLE_1_END: "gas is coming in",
    constants.CIRCLE_2_END: "gas is coming in",
    constants.CIRCLE_3_END: "gas is coming in",
    constants.CIRCLE_4_END: "gas is coming in",
    constants.CIRCLE_5_END: "gas is coming in",
    constants.LOADOUT_DROP_1: "loadout drop coming in",
    constants.LOADOUT_DROP_2: "loadout drop coming in"
}

checkpoints = list(checkpoints_messages_map.keys())