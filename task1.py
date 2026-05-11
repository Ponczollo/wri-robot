#!/usr/bin/env python3

from ev3dev2.motor import OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.button import Button
from time import sleep

tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)

left_sensor = ColorSensor(INPUT_1)
right_sensor = ColorSensor(INPUT_2)
button = Button()

BASE_SPEED = 6
TURN_SPEED = 8
TURN_SPEED_BACK = 12

SLEEP_AFTER_MODE_CHANGE = 0.025
LOOP_DELAY = 0.01


BLACK = [((0, 50), (0, 50), (0, 50))]
GREEN = [((0, 30), (40, 90), (30, 80))]
RED = [((90, 255), (0, 50), (0, 50))]
WHITE = [((90, 255), (90, 255), (90, 255))]

COLOR_RANGES =[
    BLACK,
    GREEN,
    RED,
    WHITE
]



BLACK_IDX = 0


def setup_sensors():
    left_sensor.mode = ColorSensor.MODE_RGB_RAW
    right_sensor.mode = ColorSensor.MODE_RGB_RAW
    sleep(SLEEP_AFTER_MODE_CHANGE)


def read_rgb(sensor):
    rgb = sensor.raw
    return rgb[0], rgb[1], rgb[2]


def rgb_fits_range(rgb, rgb_range):
    r, g, b = rgb
    (r_min, r_max), (g_min, g_max), (b_min, b_max) = rgb_range

    return (
        r_min <= r <= r_max and
        g_min <= g <= g_max and
        b_min <= b <= b_max
    )


def match_rgb_index(rgb, color_ranges):
    """
    Returns the index of the first matching RGB range.
    Returns -1 if the RGB reading does not fit any range.
    """
    for idx, rgb_range in enumerate(color_ranges):
        if rgb_fits_range(rgb, rgb_range):
            return idx

    return -1


def is_black(rgb):
    return match_rgb_index(rgb, COLOR_RANGES) == BLACK_IDX


def drive(left_speed, right_speed):
    tank_drive.on(SpeedPercent(left_speed), SpeedPercent(right_speed))


def forward():
    drive(BASE_SPEED, BASE_SPEED)


def turn_left():
    drive(-TURN_SPEED_BACK, TURN_SPEED)


def turn_right():
    drive(TURN_SPEED, -TURN_SPEED_BACK)


def wait_for_press():
    print("Press any button to start...")

    while not button.any():
        sleep(0.01)

    while button.any():
        sleep(0.01)


def wait_for_stop():
    if button.any():
        while button.any():
            sleep(0.01)
        return True

    else:
        left_rgb = read_rgb(left_sensor)
        right_rgb = read_rgb(right_sensor)
        left_idx = match_rgb_index(left_rgb, COLOR_RANGES)
        right_idx = match_rgb_index(right_rgb, COLOR_RANGES)
        print("LEFT:", left_rgb, "idx:", left_idx, "RIGHT:", right_rgb, "idx:", right_idx)
    return False


setup_sensors()

SEARCH_GREEN = 0
FOLLOW_GREEN = 1
RETURN_GREEN = 2
state = SEARCH_GREEN

while True:
    wait_for_press()

    try:
        while True:
            print(state)
            if wait_for_stop():
                print("Stopped.")
                tank_drive.off()
                break
                
            left_rgb = read_rgb(left_sensor)
            right_rgb = read_rgb(right_sensor)
            if state == SEARCH_GREEN:
                left_idx = match_rgb_index(left_rgb, BLACK + GREEN)
                right_idx = match_rgb_index(right_rgb, BLACK + GREEN)
                print("LEFT:", left_rgb, "idx:", left_idx, "RIGHT:", right_rgb, "idx:", right_idx)

                if left_idx == 0 and right_idx == -1:
                    turn_left()

                elif left_idx == -1 and right_idx == 0:
                    turn_right()

                elif left_idx == 1 or right_idx == 1:
                    state = FOLLOW_GREEN
                    print(state)

                    if left_idx == 1:
                        turn_left()
                        sleep(3)
                    else:
                        turn_right()
                        sleep(3)

                else:
                    forward()

            # Debug
            # print("LEFT:", left_rgb, "idx:", left_idx, "RIGHT:", right_rgb, "idx:", right_idx)

            # if left_black and right_black:
            #     forward()

            # elif not left_black and right_black:
            #     turn_right()

            # elif left_black and not right_black:
            #     turn_left()

            # else:
            #     forward()

            # sleep(LOOP_DELAY)

    finally:
        tank_drive.off()