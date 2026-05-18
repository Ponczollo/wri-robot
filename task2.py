#!/usr/bin/env python3

from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, MediumMotor
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.button import Button
from time import sleep

tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)
lift_motor = MediumMotor(OUTPUT_C)

left_sensor = ColorSensor(INPUT_1)
right_sensor = ColorSensor(INPUT_2)
button = Button()

BASE_SPEED = 8
TURN_SPEED = 10
TURN_SPEED_BACK = -14

BACK_BASE_SPEED = -8
BACK_TURN_SPEED = -10
BACK_TURN_SPEED_BACK = 10

SLEEP_AFTER_MODE_CHANGE = 0.025
LOOP_DELAY = 0.01
TURN_90_LENGTH = 1
TURN_180_LENGTH = 5
SMALL_FORWARD_LENGTH = 1
LIFT_SPEED = 10
LIFT_ROTATIONS = 0.25

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


SEARCH_GREEN = 0
GREEN_ON_LEFT = 1
GREEN_ON_RIGHT = 2
SEARCH_LANDING = 3
PICK_UP_ITEM = 4
RETURN_TO_TRACK = 5
ENTER_TRACK = 6
SEARCH_RED = 7
RED_ON_LEFT = 8
RED_ON_RIGHT = 9
RUN_FINISHED = 100

state = SEARCH_GREEN


wait_for_press()

try:
    while True: 
        if state == SEARCH_GREEN:
            setup_sensors(MODE_RGB)
            while True:
                lr, lg, lb = read_rgb(left_sensor)
                rr, rg, rb = read_rgb(right_sensor)
                l_dark = lr + lg + lb < 120
                r_dark = rr + rg + rb < 120
                if l_dark and r_dark:
                    drive(BASE_SPEED, BASE_SPEED)
                    continue
                if l_dark:
                    drive(TURN_SPEED_BACK, TURN_SPEED)
                    continue
                if r_dark:
                    drive(TURN_SPEED, TURN_SPEED_BACK)
                    continue

                l_green = (lg + lb > 3 * lr) and (lr < 30)
                r_green = (rg + rb > 3 * rr) and (rr < 30)

                if l_green:
                    state = GREEN_ON_LEFT
                    break
                if r_green:
                    state = GREEN_ON_RIGHT
                    break

                drive(BASE_SPEED, BASE_SPEED)
        

        if state == GREEN_ON_LEFT:
            drive(TURN_SPEED_BACK, TURN_SPEED * 2)
            sleep(TURN_90_LENGTH)
            state = SEARCH_LANDING


        if state == GREEN_ON_RIGHT:
            drive(TURN_SPEED * 2, TURN_SPEED_BACK)
            sleep(TURN_90_LENGTH)
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
                    drive(TURN_SPEED_BACK, TURN_SPEED)
                    continue
                if r_dark:
                    drive(TURN_SPEED, TURN_SPEED_BACK)
                    continue
                drive(BASE_SPEED, BASE_SPEED)


        if state == PICK_UP_ITEM:
            tank_drive.off()
            lift_motor.on_for_rotations(SpeedPercent(LIFT_SPEED), LIFT_ROTATIONS, block=True, brake=True)
            state = RETURN_TO_TRACK
            drive(-TURN_SPEED, TURN_SPEED)
            sleep(TURN_180_LENGTH)
            tank_drive.off()


        if state == RETURN_TO_TRACK:
            setup_sensors(MODE_REFLECT)
            while True:
                li = read_intensity(left_sensor)
                ri = read_intensity(right_sensor)
                l_dark = li < DARK_THRESHOLD
                r_dark = ri < DARK_THRESHOLD
                if l_dark and r_dark:
                    state = ENTER_TRACK
                    break
                if l_dark:
                    drive(TURN_SPEED_BACK, TURN_SPEED)
                    continue
                if r_dark:
                    drive(TURN_SPEED, TURN_SPEED_BACK)
                    continue
                drive(BASE_SPEED, BASE_SPEED)


        if state == ENTER_TRACK:
            drive(TURN_SPEED_BACK, TURN_SPEED * 2)
            sleep(TURN_90_LENGTH)
            state = SEARCH_RED


        if state == SEARCH_RED:
            setup_sensors(MODE_RGB)
            while True:
                lr, lg, lb = read_rgb(left_sensor)
                rr, rg, rb = read_rgb(right_sensor)
                l_dark = lr + lg + lb < 100
                r_dark = rr + rg + rb < 100
                if l_dark and r_dark:
                    drive(BASE_SPEED, BASE_SPEED)
                    continue
                if l_dark:
                    drive(TURN_SPEED_BACK, TURN_SPEED)
                    continue
                if r_dark:
                    drive(TURN_SPEED, TURN_SPEED_BACK)
                    continue

                l_red = (lr > (lg + lb)) and (lr > 100)
                r_red = (rr > (rg + rb)) and (rr > 100)

                if l_red:
                    state = RED_ON_LEFT
                    break
                if r_red:
                    state = RED_ON_RIGHT
                    break

                drive(BASE_SPEED, BASE_SPEED)

        if state == RED_ON_LEFT:
            print("RED ON LEFT")
            state = RUN_FINISHED

        if state == RED_ON_RIGHT:
            print("RED ON RIGHT")
            state = RUN_FINISHED

        if state == RUN_FINISHED:
            tank_drive.off()
            break



finally:
    tank_drive.off()
    lift_motor.off(brake=True)
