'''
Author:         Waqas Ali
Project Name:   Gesture Controlled Articulated Robotic Arm
                argumented with Computer Vision
Description:    This is the code to transform coordinated of end effector into 
                joint angles 
Inputs:         Coordinates of end effector in 3D Space
Outputs:        Joint angles
Created on:     Aug 2023
Copy Rights:    Waqas Ali Shah "waqas.ali.shah2@gmail.com"
'''
import math as m

# Define configuration parameters
L1 = 210
L2 = 170
L3 = 350

# Define the math functions
asin = m.asin
acos = m.acos
atan2 = m.atan2
atan = m.atan
sqrt = m.sqrt
cos = m.cos
sin = m.sin

def inverse(position):

    # Input coordinates of end point
    x_end = Px = position[0]
    y_end = Py = position[1]
    z_end = position[2]
    #test for coordinates within the workspace
    if x_end>L2+L3 or y_end>L2+L3 or z_end>L1+L2+L3:
        print ("Out of space")
        return [0,0,0]
    
    Pz = z_end - L1
    theta1 = atan2(Py,Px)
    theta1_d=180*theta1/m.pi
       
    print ("Test for theta2: " + str((Px**2+Py**2+Pz**2<L2**2+L3**2)))
    theta3 = acos((Px**2+Py**2+Pz**2-L2**2-L3**2)/(2*L2*L3))
    theta3_d=180*theta3/m.pi

    
    beta=atan(Pz/sqrt(Px**2+Py**2))
    cos_gama=(L2**2+Px**2+Py**2+Pz**2-L3**2)/(2*L2*sqrt(Px**2+Py**2+Pz**2))
    sin_gama=sqrt(1-cos_gama**2)
    gama=atan2(-sin_gama,cos_gama)
    gama1=atan2(sin_gama,cos_gama)
    
    theta2 = beta+gama
    theta2a = beta+gama1
    
    theta2_d=180*theta2/m.pi
    theta2a_d=180*theta2a/m.pi
    print ("The ambiguous angles are: "+str(theta2_d) + " and " + str(theta2a_d))
    return [theta1_d,theta2_d,theta3_d]
