import constants
import math
from message import Message

__all__ = ["create"]

_checkpoint_message_map = {
    constants.GAME_START_CUT_SCENE: "match is starting",
    constants.CIRCLE_1_END: "gas is coming in",
    constants.CIRCLE_2_END: "gas is coming in",
    constants.CIRCLE_3_END: "gas is coming in",
    constants.CIRCLE_4_END: "gas is coming in",
    constants.CIRCLE_5_END: "gas is coming in",
    constants.LOADOUT_DROP_1: "loadout drop coming in",
    constants.LOADOUT_DROP_2: "loadout drop coming in"
}

# Since we're working with real wall-clock time to determine in-game checkpoints,
# we can't assume that our code executes every second. To account for the occasional
# miss, let's include the checkpoint time +/- one second.
_map_copy = _checkpoint_message_map.copy()
for key, value in _checkpoint_message_map.items():
    _map_copy[key + 1] = value
    _map_copy[key] = value
    _map_copy[key - 1] = value
_checkpoint_message_map.clear()
_checkpoint_message_map = _map_copy

_checkpoints = list(_checkpoint_message_map.keys())

def create(cash_total, buy_back_count, time_elapsed):
    time_elapsed = int(time_elapsed)

    if (time_elapsed not in _checkpoints and
        (cash_total < constants.BUY_BACK_COST or 
            (cash_total < constants.LOADOUT_COST and buy_back_count == 0))):

        # To avoid sending too many un-useful messages, let's only send a message
        # if we can:
        # 1. afford a loadout
        # 2. we need to buy a player back
        # 3. time has elapsed onto a checkpoint
        return Message(None, None)
    
    message = "Total cash is ${}".format(cash_total)

    if (cash_total >= constants.LOADOUT_COST and 
        cash_total <= constants.LOADOUT_COST * 2):

        # Send a message if they can afford a loadout drop but don't send a 
        # message if they have double the amount needed because it is obvious
        # at that point and we want to reduce the number of disruptive messages
        message += ", you can buy a loadout drop"
        if (buy_back_count >= 1):
            message += " or"

    if (buy_back_count >= 1 and cash_total >= constants.BUY_BACK_COST):
        buy_back_amount = math.floor(cash_total / constants.BUY_BACK_COST)
        message += ", you can buy back {} of your teammates".format(
            min(buy_back_amount, buy_back_count))
    
    messageObject = Message(message, "loadout_cash_prompt") \
        if "loadout" in message \
        else Message(message, "cash_prompt")

    if (time_elapsed in _checkpoints):
        message = _checkpoint_message_map[time_elapsed]
        messageObject = Message(message, "checkpoint")

    return messageObject