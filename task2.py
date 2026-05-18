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

BASE_SPEED = 8
TURN_SPEED = 10
TURN_SPEED_BACK = 14

SLEEP_AFTER_MODE_CHANGE = 0.025
LOOP_DELAY = 0.01
HARD_TURN_LENGTH = 1

MODE_REFLECT = ColorSensor.MODE_COL_REFLECT
MODE_RGB = ColorSensor.MODE_RGB_RAW

DARK_THRESHOLD = 25

def setup_sensors(mode):
    left_sensor.mode = mode
    right_sensor.mode = mode
    sleep(SLEEP_AFTER_MODE_CHANGE)


def read_rgb(sensor):
    rgb = sensor.raw
    return rgb[0], rgb[1], rgb[2]


def read_intensity(sensor):
    return sensor.reflected_light_intensity


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
    return False


setup_sensors(MODE_RGB)

SEARCH_GREEN = 0
GREEN_ON_LEFT = 1
GREEN_ON_RIGHT = 2
SEARCH_LANDING = 3
PICK_UP_ITEM = 4
RETURN_GREEN = ...
SEARCH_RED = ...
RED_ON_LEFT = ...
RED_ON_RIGHT = ...

state = SEARCH_GREEN



wait_for_press()

try:
    while True: 
        if state == SEARCH_GREEN:
            while True:
                lr, lg, lb = read_rgb(left_sensor)
                rr, rg, rb = read_rgb(right_sensor)
                l_dark = lr + lg + lb < 120
                r_dark = rr + rg + rb < 120
                if l_dark and r_dark:
                    forward()
                    continue
                if l_dark:
                    turn_left()
                    continue
                if r_dark:
                    turn_right()
                    continue

                l_green = (lg + lb > 3 * lr) #and (lr < 30)
                r_green = (rg + rb > 3 * rr) #and (rr < 30)

                if l_green:
                    state = GREEN_ON_LEFT
                    break
                if r_green:
                    state = GREEN_ON_RIGHT
                    break

                forward()
        

        if state == GREEN_ON_LEFT:
            turn_left()
            sleep(HARD_TURN_LENGTH)
            state = SEARCH_LANDING


        if state == GREEN_ON_RIGHT:
            turn_right()
            sleep(HARD_TURN_LENGTH)
            state = SEARCH_LANDING
        

        if state == SEARCH_LANDING:
            setup_sensors(MODE_REFLECT)
            while True:
                li = read_intensity(left_sensor)
                ri = read_intensity(right_sensor)
                l_dark = li < DARK_THRESHOLD
                r_dark = ri < DARK_THRESHOLD
                if l_dark and r_dark:
                    state = PICK_UP_ITEM
                    break
                if l_dark:
                    turn_left()
                    continue
                if r_dark:
                    turn_right()
                    continue
                forward()


        if state == PICK_UP_ITEM:
            ...



finally:
    tank_drive.off()