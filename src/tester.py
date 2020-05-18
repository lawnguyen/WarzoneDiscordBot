from timer import Timer
import constants
import time

time_map = {
    constants.GAME_START_CUT_SCENE: "game started",
    constants.CIRCLE_1_END: "circle 1 end",
    constants.CIRCLE_2_END: "circle 2 end",
    constants.CIRCLE_3_END: "circle 3 end",
    constants.CIRCLE_4_END: "circle 4 end",
    constants.CIRCLE_5_END: "circle 5 end",
    constants.CIRCLE_6_END: "circle 6 end",
    constants.CIRCLE_7_END: "circle 7 end",
    constants.LOADOUT_DROP_1: "loadout 1 incoming",
    constants.LOADOUT_DROP_2: "loadout 2 incoming"
}

def test():     
    _timer = Timer()
    _timer.restart_timer()
    while(1):
        time.sleep(0.5)
        elapsed = int(_timer.get_time_elapsed())
        if (elapsed in list(time_map.keys())):
            print(time_map[elapsed])