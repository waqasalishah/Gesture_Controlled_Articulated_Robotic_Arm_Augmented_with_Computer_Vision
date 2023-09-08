'''
Author:         Waqas Ali
Project Name:   Gesture Controlled Articulated Robotic Arm
                argumented with Computer Vision
Description:    This is moves open/closes the end effector. The opening is dependent
                on the input angle
Inputs:         Closing angles (0 to 90)
Outputs:        None
Created on:     Aug 2023
Copy Rights:    Waqas Ali Shah "waqas.ali.shah2@gmail.com"
'''

from gpiozero import AngularServo
import time

# Brown    GND
# Orange   Power
# Yellow   Signal


servo = AngularServo(6,min_angle=0, max_angle=180, min_pulse_width=0.0005,max_pulse_width=0.0025)



def end_effector(servoAngle):
    if servoAngle > 100 or servoAngle < 0:
        servo.angle = 100
    else:
        servo.angle = servoAngle
    return servoAngle




