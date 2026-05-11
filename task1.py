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

def setup_sensors():
    left_sensor.mode = ColorSensor.MODE_RGB_RAW
    right_sensor.mode = ColorSensor.MODE_RGB_RAW
    sleep(SLEEP_AFTER_MODE_CHANGE)


def read_rgb(sensor):
    rgb = sensor.raw
    return rgb[0], rgb[1], rgb[2]


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


setup_sensors()

SEARCH_GREEN = 0
GREEN_ON_LEFT = 1
GREEN_ON_RIGHT = 2
RED_ON_LEFT = 3
RED_ON_RIGHT = 4
RETURN_GREEN = 10
state = SEARCH_GREEN

while True:
    wait_for_press()

    try:
        while True:
            # if wait_for_stop():
            #     print("Stopped.")
            #     tank_drive.off()
            #     break
                
            lr, lg, lb = read_rgb(left_sensor)
            rr, rg, rb = read_rgb(right_sensor)
            l_black = lr + lg + lb < 120
            r_black = rr + rg + rb < 120
            if state == SEARCH_GREEN:
                if l_black and r_black:
                    forward()
                    continue
                if l_black:
                    turn_left()
                    continue
                if r_black:
                    turn_right()
                    continue

                forward()

                # if lr > 100 and lg + lb < 80:
                #     print("RED ON RIGHT")

                # if rr > 100 and rg + rb < 80:
                #     print("RED ON RIGHT")

                # if lr < 50 and lg + lb > 100:
                #     print("GREEN ON LEFT")

                # if rr < 50 and rg + rb > 100:
                #     print("GREEN ON RIGHT")


    finally:
        tank_drive.off()