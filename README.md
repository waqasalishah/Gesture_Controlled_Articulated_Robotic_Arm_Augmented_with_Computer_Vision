# Articulated_Robotic_Arm

The connection pins are as:-

-------------------------------
For Stepper Motor
-------------------------------

# Direction pin from Raspberry Pi controller
DIR = [17, 27, 22] #Yellow wires

# Steps pin from Raspberry Picontroller
PUL = [18, 23, 24] # Green

-------------------------------
For End Effector Servo Motor
-------------------------------

End Effector servo motor signal pin
pin 6 # Yellow control pin





-------------------------------
Control of Program
-------------------------------
This includes the 4 proograms

# Main control 0:
It rotates the each joint with user angle input in the run time.

# Main control 1:
It creates the GUI to input the angle and keep track the home position of the robotic arm. 
Whenever we input the angle the robotic arm moves with reference to the home position.

# Main control 2:
This program roates the joints using gestrure control and MQTT principle is utilized
 to for the wireless communication.

# Main control 3:
This program has two stages. The first stage is it capture the video from the camera and display
in a windows and it recognises the person face from the stored data.
The second stage is stats when we pree q key form the keyboard.
In the second stage the it captrues the video for 20 seconds if the face is recognized with
ore than 80% of the accuracy then the robotic arm moves.

