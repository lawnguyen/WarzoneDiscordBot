import constants
import math
from message import Message

__all__ = ["create"]

def _add_time_buffer(checkpoint_map):
    map_copy = {}	
    for key, value in checkpoint_map.items():	
        map_copy[key + 1] = value	
        map_copy[key] = value	
        map_copy[key - 1] = value	
    checkpoint_map.clear()	
    return map_copy

_heads_up_time_loadout = 30 # in seconds
_heads_up_time_gas = 10 # in seconds
_path_to_audio_files = "./audio/"

_checkpoint_message_map = {
    constants.GAME_START_CUT_SCENE: "match is starting",
    constants.CIRCLE_1_END - _heads_up_time_gas: "gas is coming in {}".format(_heads_up_time_gas),
    constants.CIRCLE_2_END - _heads_up_time_gas: "gas is coming in {}".format(_heads_up_time_gas),
    constants.CIRCLE_3_END - _heads_up_time_gas: "gas is coming in {}".format(_heads_up_time_gas),
    constants.CIRCLE_4_END - _heads_up_time_gas: "gas is coming in {}".format(_heads_up_time_gas),
    constants.CIRCLE_5_END - _heads_up_time_gas: "gas is coming in {}".format(_heads_up_time_gas),
    constants.CIRCLE_1_END + int(constants.CIRCLE_1_MOVING / 2): "gas is halfway in",
    constants.CIRCLE_2_END + int(constants.CIRCLE_2_MOVING / 2): "gas is halfway in",
    constants.CIRCLE_3_END + int(constants.CIRCLE_3_MOVING / 2): "gas is halfway in",
    constants.CIRCLE_4_END + int(constants.CIRCLE_4_MOVING / 2): "gas is halfway in",
    constants.CIRCLE_5_END + int(constants.CIRCLE_5_MOVING / 2): "gas is halfway in",
    constants.LOADOUT_DROP_1 - _heads_up_time_loadout: "loadout drop coming in {} seconds".format(_heads_up_time_loadout),
    constants.LOADOUT_DROP_2 - _heads_up_time_loadout: "loadout drop coming in {} seconds".format(_heads_up_time_loadout)
}

_checkpoint_audio_path_map = {
    constants.GAME_START_CUT_SCENE: _path_to_audio_files + "match_start.mp3",
    constants.CIRCLE_1_END - _heads_up_time_gas: _path_to_audio_files + "gas_is_coming_in_10.mp3",
    constants.CIRCLE_2_END - _heads_up_time_gas: _path_to_audio_files + "gas_is_coming_in_10.mp3",
    constants.CIRCLE_3_END - _heads_up_time_gas: _path_to_audio_files + "gas_is_coming_in_10.mp3",
    constants.CIRCLE_4_END - _heads_up_time_gas: _path_to_audio_files + "gas_is_coming_in_10.mp3",
    constants.CIRCLE_5_END - _heads_up_time_gas: _path_to_audio_files + "gas_is_coming_in_10.mp3",
    constants.CIRCLE_1_END + int(constants.CIRCLE_1_MOVING / 2): _path_to_audio_files + "gas_is_halfway_in.mp3",
    constants.CIRCLE_2_END + int(constants.CIRCLE_2_MOVING / 2): _path_to_audio_files + "gas_is_halfway_in.mp3",
    constants.CIRCLE_3_END + int(constants.CIRCLE_3_MOVING / 2): _path_to_audio_files + "gas_is_halfway_in.mp3",
    constants.CIRCLE_4_END + int(constants.CIRCLE_4_MOVING / 2): _path_to_audio_files + "gas_is_halfway_in.mp3",
    constants.CIRCLE_5_END + int(constants.CIRCLE_5_MOVING / 2): _path_to_audio_files + "gas_is_halfway_in.mp3",
    constants.LOADOUT_DROP_1 - _heads_up_time_loadout: _path_to_audio_files + "loadout_is_coming_in_30s.mp3",
    constants.LOADOUT_DROP_2 - _heads_up_time_loadout: _path_to_audio_files + "loadout_is_coming_in_30s.mp3"
}

# Since we're working with real wall-clock time to determine in-game checkpoints,	
# we can't assume that our code executes every second. To account for the occasional	
# miss, let's include the checkpoint time +/- one second.		
_checkpoint_message_map = _add_time_buffer( _checkpoint_message_map.copy())		
_checkpoint_audio_path_map = _add_time_buffer(_checkpoint_audio_path_map.copy())

_checkpoints = list(_checkpoint_message_map.keys())

def create(cash_total, buy_back_count, time_elapsed):
    time_elapsed = int(time_elapsed)

    if (time_elapsed in _checkpoints):
        # Send checkpoint message
        message = _checkpoint_message_map[time_elapsed]
        audio = _checkpoint_audio_path_map[time_elapsed]
        messageObject = Message(message, "checkpoint", audio)
        return messageObject
    elif (not cash_total):
        # No message if not checkpoint or there's no cash total
        return Message(None, None, None)

    if (cash_total < constants.BUY_BACK_COST or 
            (cash_total < constants.LOADOUT_COST and buy_back_count == 0)):

        # To avoid sending too many un-useful messages, let's only send a message
        # if we can:
        # 1. afford a loadout
        # 2. we need to buy a player back
        # 3. time has elapsed onto a checkpoint
        return Message(None, None, None)
    
    # There is a cash total, so create a message for it
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
    
    if "loadout" in message:
        audio = _path_to_audio_files + "afford_loadout.mp3"
        messageObject = Message(message, "loadout_cash_prompt", audio)
    elif "buy back" in message:
        # TODO: Implement audio for > 1 buy back
        audio = _path_to_audio_files + "buy_back_1_teammates.mp3"
        messageObject = Message(message, "cash_prompt", audio)
    else:
        messageObject = Message(None, "none", None)

    return messageObject