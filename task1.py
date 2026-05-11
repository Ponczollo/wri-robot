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

BASE_SPEED = 12
TURN_SPEED = 16
TURN_SPEED_BACK = 20

BLACK_THRESHOLD = 25

SLEEP_AFTER_MODE_CHANGE = 0.025
LOOP_DELAY = 0.01


def left_intensity():
    return left_sensor.reflected_light_intensity


def right_intensity():
    return right_sensor.reflected_light_intensity


def is_black(value):
    return value < BLACK_THRESHOLD


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
    while button.any():  # wait for release
        sleep(0.01)


def wait_for_stop():
    if button.any():
        while button.any():
            sleep(0.01)
        return True
    return False


while True:
    wait_for_press()

    try:
        while True:
            if wait_for_stop():
                print("Stopped.")
                tank_drive.off()
                break

            left_value = left_intensity()
            right_value = right_intensity()

            left_black = is_black(left_value)
            right_black = is_black(right_value)

            if left_black and right_black:
                forward()

            elif not left_black and right_black:
                turn_right()

            elif left_black and not right_black:
                turn_left()

            else:
                forward()

            sleep(LOOP_DELAY)

    finally:
        tank_drive.off()