#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_C, MediumMotor, SpeedPercent

lift_motor = MediumMotor(OUTPUT_C)

LIFT_SPEED = 10
LIFT_ROTATIONS = 0.25

lift_motor.on_for_rotations(SpeedPercent(LIFT_SPEED), LIFT_ROTATIONS, block=True, brake=True)