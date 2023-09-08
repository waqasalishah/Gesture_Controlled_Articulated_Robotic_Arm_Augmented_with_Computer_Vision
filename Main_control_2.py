'''
Author:         Waqas Ali
Project Name:   Gesture Controlled Articulated Robotic Arm
                argumented with Computer Vision
Description:    This file connects to Mosquitto broker then receives data from
                from the Glove Controller (ESP32) and end effector and joints are
                moved according to the orientation of hand
Inputs:         Hand Orientation from the glove controller
Outputs:        Hardware joint rotation
Created on:     Aug 2023
Copy Rights:    Waqas Ali Shah "waqas.ali.shah2@gmail.com"
'''
import time
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

from alpha_servo import end_effector
from alpha_joint_motion import all_rotation 
from alpha_joint_motion import angle_buff
from alpha_joint_motion import joint_rotation

from alpha_inverse_kinematics import inverse
from alpha_forward_kinematics import forward


# Broker addr and port for Home network
BROKER_ADDR = "192.168.1.205"
BROKER_POART = 1883

# Broker addr and port for LAPTOP
BROKER_ADDR = "192.168.137.124"
BROKER_POART = 1883


# Topic of subscription
MQTT_TOPIC_0 = "main"
MQTT_TOPIC_1 = "main/glove/flex"
MQTT_TOPIC_2 = "main/glove/angle"
# Angle data from ESP32
angle_data = [0,0,0,0,0,0,0,0,0]
joint_motion = [0,0,0]

gripper = 0
joint_angle_posn = [0,0,0]
joint_angle_limits = [[-160,160],[-30,30],[-45,45]]
j1_angle_limit = 0
j2_angle_limit = 0
j3_angle_limit = 0

# Variables of this class
angles = [0,0,0]
coordinates = [0,0,0]

# Function to return to home position
def home():all_rotation([0, 0, 0])

# Definitions of MQTT functions
def on_connect(client, userdata,flags, rc):
    if rc == 0:
        print("Connected to MQTT server successfully.")
        print("Ready to receive/send data.")
    else:
        print("Connection failed. rc= "+str(rc))

def on_publish(client, userdata, mid):
    print("Message "+str(mid)+" published.")

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribe to topic: "+str(mid))

def on_message(client, userdata, msg):
    global angle_data
    #print("Message received on topic: "+str(msg.topic)+"with QoS: "+str(msg.qos))
    #print("Message is: "+str(msg.payload))
    if msg.topic == MQTT_TOPIC_2:
            msg_str = msg.payload.decode()
            msg_list = msg_str.split(',')
            #print(msg_list)
            for i in range(9):
                angle_data[i] = int(msg_list[i])- 1000*(i+1)-500
            #print(angle_data,end='\r')
    elif msg.topic == MQTT_TOPIC_1:
        print("flex data")
    elif msg.topic == MQTT_TOPIC_0:
        print(msg.payload.decode())
    else:
        print("msg topic is not recongnized")

# Initialize the MQTT and create the MQTT client
def create_mqtt_client():
    
    # Creating the client
    mqttclient = mqtt.Client("P1")

    # Connecting to the broker server
    mqttclient.connect(BROKER_ADDR)

    # Assign event callbacks
    mqttclient.on_message = on_message
    mqttclient.on_connect = on_connect
    mqttclient.on_subscribe = on_subscribe

    # Start subscription of topic 1
    mqttclient.subscribe(MQTT_TOPIC_0)
    mqttclient.subscribe(MQTT_TOPIC_1)
    mqttclient.subscribe(MQTT_TOPIC_2)

    mqttclient.loop_start()
    # Continue monitoring the incoming messages for subscribed topic
    
# Map value function maps the value of data  
def map_value(value, from_low, from_high, to_low, to_high):
    x = (value - from_low) * (to_high - to_low) / (from_high - from_low) + to_low
    return int(x)

# It check the joint angles as per the orientation of hand received from ESP32   
def check_joint_motion():
    global joint_motion
    for i in range(2):
        if -20 <= angle_data[i] < 20:
            #print("No motion")
            joint_motion[i] = 0
        else:
            joint_motion[i] = map_value(angle_data[i],-90,90,-40,40)
            
# this function rotates the joint 1 after receit of data
def J1_motion():
    global j1_angle_limit,joint_motion
    if -160 <= (j1_angle_limit+joint_motion[0]) <= 160:
        j1_angle_limit = j1_angle_limit + joint_motion[0]
        joint_rotation(1,joint_motion[0])
    else: 
        print("Maximum limit achieved")
    print("J1: "+str(j1_angle_limit))
 
# this function rotates the joint 2 and joint 3 after receit of data 
def J2_J3_motion():
    global j2_angle_limit,j3_angle_limit,joint_motion
    
    if -30 <= (j3_angle_limit+joint_motion[1]) <=30:
        j3_angle_limit = j3_angle_limit + joint_motion[1]
        joint_rotation(2,joint_motion[1])
    elif   -45 <= (j2_angle_limit+joint_motion[1]) <= 45:
        j2_angle_limit = j2_angle_limit + joint_motion[1]
        joint_rotation(3,joint_motion[1])
    else: 
        print("Maximum limit achieved")
    print("J2: "+str(j2_angle_limit))
    print("J3: "+str(j3_angle_limit))
    
    
# This function tests check the gripperand open or close the gripper data    
def check_gripper():
    global angle_data
    print(angle_data[8])
    if angle_data[8]< 3500:
        end_effector(90)
    else:
        end_effector(0)
    print("Griper:"+str(gripper))

    
    
# Start of the class
print("Starting and Initializing....")
time.sleep(1)
create_mqtt_client()
time.sleep(1)

while True:
    check_joint_motion()
    J1_motion()
    J2_J3_motion()
    check_gripper()