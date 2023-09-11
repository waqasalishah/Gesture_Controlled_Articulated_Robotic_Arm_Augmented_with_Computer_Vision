'''
Author:         Waqas Ali
Project Name:   Gesture Controlled Articulated Robotic Arm
                argumented with Computer Vision
Description:    This file connects the robotic arm to the OAK-D Camerra
                phase 1: This file display the rgb video captured from the OAK-D camera
                and faceial recogntion is done.
                Phase 2: on pressing "q" the program switches to 2nd mode. Now if
                master user appears beofore camera then robotic arm moves to bend position
                after wait of 10 seconds it move back to original position.
Inputs:         Master user appear before camera
Outputs:        hardware rotation
Created on:     Aug 2023
Copy Rights:    Waqas Ali Shah "waqas.ali.shah2@gmail.com"
'''
# coding=utf-8
import os
import argparse
import blobconverter
import cv2
import depthai as dai
import numpy as np
from MultiMsgSync import TwoStageHostSeqSync
from FaceRecognition import FaceRecognition
from TextHelper import TextHelper
from CameraSetup import CameraSetup
import time

import RPi.GPIO as GPIO

from alpha_servo import end_effector
from alpha_joint_motion import all_rotation 
from alpha_joint_motion import angle_buff
from alpha_joint_motion import joint_rotation

from alpha_inverse_kinematics import inverse
from alpha_forward_kinematics import forward




parser = argparse.ArgumentParser()
parser.add_argument("-name", "--name", type=str, help="Name of the person for database saving")

args = parser.parse_args()


cam = CameraSetup()
pipeline = cam.pipeline
databases = cam.databases


# Function to return to home position
def home():all_rotation([0, 0, 0])


def frame_norm(frame, bbox):
    normVals = np.full(len(bbox), frame.shape[0])
    normVals[::2] = frame.shape[1]
    return (np.clip(np.array(bbox), 0, 1) * normVals).astype(int)


with dai.Device(pipeline) as device:
    facerec = FaceRecognition(databases, args.name)
    sync = TwoStageHostSeqSync()
    text = TextHelper()

    queues = {}
    # Create output queues
    for name in ["color", "detection", "recognition"]:
        queues[name] = device.getOutputQueue(name)

    while True:
        for name, q in queues.items():
            # Add all msgs (color frames, object detections and face recognitions) to the Sync class.
            if q.has():
                sync.add_msg(q.get(), name)

        msgs = sync.get_msgs()
        if msgs is not None:
            frame = msgs["color"].getCvFrame()
            dets = msgs["detection"].detections

            for i, detection in enumerate(dets):
                bbox = frame_norm(frame, (detection.xmin, detection.ymin, detection.xmax, detection.ymax))
                cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (10, 245, 10), 2)

                features = np.array(msgs["recognition"][i].getFirstLayerFp16())
                conf, name = facerec.new_recognition(features)
                text.putText(frame, f"{name} {(100*conf):.0f}%", (bbox[0] + 10,bbox[1] + 35))
            cv2.imshow("color", cv2.resize(frame, (800,800)))
        if cv2.waitKey(1) == ord('q'):
            #cv2.destroyAllWindows()
            break
        
def Capture(t,start_time,result):
    with dai.Device(pipeline) as device:
        facerec = FaceRecognition(databases, args.name)
        sync = TwoStageHostSeqSync()
        text = TextHelper()
        queues = {}
        # Create output queues
        for name in ["color", "detection", "recognition"]:
            queues[name] = device.getOutputQueue(name)
        while True:
            for name, q in queues.items():
                # Add all msgs (color frames, object detections and face recognitions) to the Sync class.
                if q.has():
                    sync.add_msg(q.get(), name)

            msgs = sync.get_msgs()
            if msgs is not None:
                frame = msgs["color"].getCvFrame()
                dets = msgs["detection"].detections

                for i, detection in enumerate(dets):
                    bbox = frame_norm(frame, (detection.xmin, detection.ymin, detection.xmax, detection.ymax))
                    cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (10, 245, 10), 2)

                    features = np.array(msgs["recognition"][i].getFirstLayerFp16())
                    conf, name = facerec.new_recognition(features)
                    text.putText(frame, f"{name} {(100*conf):.0f}%", (bbox[0] + 10,bbox[1] + 35))
                    
                    if conf > 0.80:
                        #Do if accuracy is geater than 90%
                        result = max(result,conf)
                    else:
                        bend = False
            if time.time() - start_time > t*60 or result > 0.85:
                print("face detected in " + str(int(time.time() - start_time))+ " seconds")
                break
    
    return result     






print ("/n/n Welcome to Face Recognition and unlocking the Robotic Arm")
run = 0
while True:
    print("Capture for 20 seconds or till recognition of face")
    r = Capture(0.1,time.time(),0)
    print("Confidance level "+str(r*100))
    
    if r > 0.70:
        all_rotation([-90, -10, -45])
    else:
        home()
        
    run =run + 1
    print(run)
    if run == 20:
        break
