from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.led import Leds
from ev3dev2.button import Button

tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)
# tank_drive.on_for_rotations(SpeedPercent(20), SpeedPercent(20), 0.5)

BLACK = 1
GREEN = 3
RED = 5
WHITE = 6

left_sensor = ColorSensor(INPUT_1)
right_sensor = ColorSensor(INPUT_2)

button = Button()

def turn_left():
    tank_drive.on_for_seconds(SpeedPercent(-14), SpeedPercent(7), 0.2)

def turn_right():
    tank_drive.on_for_seconds(SpeedPercent(7), SpeedPercent(-14), 0.2)

def forward():
    tank_drive.on_for_seconds(SpeedPercent(7), SpeedPercent(7), 0.2)

while True:
    
    move_right = 0
    move_left = 0
    if left_sensor.color == BLACK and right_sensor.color == BLACK :
        forward()
    if left_sensor.color != BLACK and right_sensor.color == BLACK :
        turn_right()
    if left_sensor.color == BLACK and right_sensor.color != BLACK :
        turn_left()
    if left_sensor.color != BLACK and right_sensor.color != BLACK :
        forward()
    # print("LEFT: ",end='')
    # if left_sensor.color != BLACK:
    #     print("WHITE",end='')
    #     move_left += 5
    # elif left_sensor.color == BLACK:
    #     print("BLACK",end='')
    #     move_right += 10
    #     move_left -= 5
    # print("\nRIGHT: ",end='')
    # if right_sensor.color != BLACK:
    #     print("WHITE",end='')
    #     move_right += 5
    # elif right_sensor.color == BLACK:
    #     print("BLACK",end='')
    #     move_left += 10
    #     move_right -= 5
    # tank_drive.on_for_seconds(SpeedPercent(move_left), SpeedPercent(move_right), 0.3)
