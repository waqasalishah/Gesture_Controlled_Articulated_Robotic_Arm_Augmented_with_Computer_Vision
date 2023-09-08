'''
Author:         Waqas Ali
Project Name:   Gesture Controlled Articulated Robotic Arm
                argumented with Computer Vision
Description:    This file produces the GUI to input the angles and end effector opening
                and then on pressing the button the end effector moves.
Inputs:         User input of angles
Outputs:        Hardware joint rotation
Created on:     Aug 2023
Copy Rights:    Waqas Ali Shah "waqas.ali.shah2@gmail.com"
'''
import RPi.GPIO as GPIO
import time


from guizero import App,Text,TextBox,PushButton,Picture

from alpha_servo import end_effector
from alpha_joint_motion import all_rotation 
from alpha_joint_motion import angle_buff
from alpha_joint_motion import joint_rotation


# Function to return to home position
def home():
    all_rotation([0, 0, 0])
    print("Moved to home posn")

def Rotate():
    msg = "Rotating Joint 1: " + joint_1.value + " degrees. joint 2: "+ joint_2.value + " degrees. joint 3: " +joint_3.value + " degrees."
    print(msg)
    all_rotation([int(joint_1.value), int(joint_2.value), int(joint_3.value)])
    print("Roation complete")
    time.sleep(1)
    end_effector(int(end_effector_state.value))
    print("End Effector movement completed")




# Start of the class
print("Starting and Initializing....")
time.sleep(1)

# Displaying the GUI for joint motion
app = App(layout="grid",title = "Articulated Robotic Arm : Zortrax")
welcome_msg = Text(app,text="Welcome to the joint control of Robotic Arm",
                   size=20, font="Times New Roman",color="blue")  

Text(app,grid=[0,0],align="left",text="   Enter gripper opening angle (0-90):")
end_effector_state = TextBox(app,width=20,grid=[1,0])
Text(app,grid=[0,1]) # Leaves some space 

Text(app,grid=[0,2],align="left",text="   Enter Joint 1 angle (-160 to +160):")
joint_1 = TextBox(app,width=20,grid=[1,2])


Text(app,grid=[0,3],align="left",text="   Enter Joint 2 angle (-45 to +45):")
joint_2 = TextBox(app,width=20,grid=[1,3])


Text(app,grid=[0,4],align="left",text="   Enter Joint 3 angle (-90 to +90):")
joint_3 = TextBox(app,width=20,grid=[1,4])
Text(app,grid=[0,5]) # Leaves some space 

# Pressing the Push Button execute the rotation command
B1 = PushButton(app,grid=[1,6],command=Rotate, text="Move the joints")
Text(app,grid=[0,7]) # Leaves some space 
picture_1 = Picture(app,grid=[0,8,2,1],image="/home/pi/Desktop/Articulated_Robotic_Arm/Robotic_arm_an.jpeg")
Text(app,grid=[0,9]) # Leaves some space

# Pressing the Push Button execute the rotation command
B2 = PushButton(app,grid=[1,10],command=home, text="Move to Home Posn")
Text(app,grid=[0,11])  # Leaves some space 
Text(app,grid=[1,12],text="Designed by Ali Waqas \n MSc Student at UoN \n version: 0.0.7")
    