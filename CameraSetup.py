'''
Author:         Waqas Ali
Project Name:   Gesture Controlled Articulated Robotic Arm
                argumented with Computer Vision
Description:    This code file initialises the OAK-D Camera with node connection
                and input and output configurations.  
Inputs:         None
Outputs:        None
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



class CameraSetup:

    def __init__(self):
        VIDEO_SIZE = (1072, 1072)
        databases = "databases"
        self.databases = databases
        if not os.path.exists(databases):
            os.mkdir(databases)
        print("Creating pipeline...")
        pipeline = dai.Pipeline()
        self.pipeline = pipeline

        print("Creating Color Camera...")
        cam = pipeline.create(dai.node.ColorCamera)
        # For ImageManip rotate you need input frame of multiple of 16
        cam.setPreviewSize(1072, 1072)
        cam.setVideoSize(VIDEO_SIZE)
        cam.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
        cam.setInterleaved(False)
        cam.setBoardSocket(dai.CameraBoardSocket.RGB)

        host_face_out = pipeline.create(dai.node.XLinkOut)
        host_face_out.setStreamName('color')
        cam.video.link(host_face_out.input)

        # ImageManip as a workaround to have more frames in the pool.
        # cam.preview can only have 4 frames in the pool before it will
        # wait (freeze). Copying frames and setting ImageManip pool size to
        # higher number will fix this issue.
        copy_manip = pipeline.create(dai.node.ImageManip)
        cam.preview.link(copy_manip.inputImage)
        copy_manip.setNumFramesPool(20)
        copy_manip.setMaxOutputFrameSize(1072*1072*3)

        # ImageManip that will crop the frame before sending it to the Face detection NN node
        face_det_manip = pipeline.create(dai.node.ImageManip)
        face_det_manip.initialConfig.setResize(300, 300)
        copy_manip.out.link(face_det_manip.inputImage)

        # NeuralNetwork
        print("Creating Face Detection Neural Network...")
        face_det_nn = pipeline.create(dai.node.MobileNetDetectionNetwork)
        face_det_nn.setConfidenceThreshold(0.5)
        face_det_nn.setBlobPath(blobconverter.from_zoo(name="face-detection-retail-0004", shaves=6))
        # Link Face ImageManip -> Face detection NN node
        face_det_manip.out.link(face_det_nn.input)

        face_det_xout = pipeline.create(dai.node.XLinkOut)
        face_det_xout.setStreamName("detection")
        face_det_nn.out.link(face_det_xout.input)

        # Script node will take the output from the face detection NN as an input and set ImageManipConfig
        # to the 'age_gender_manip' to crop the initial frame
        script = pipeline.create(dai.node.Script)
        script.setProcessor(dai.ProcessorType.LEON_CSS)

        face_det_nn.out.link(script.inputs['face_det_in'])
        # We also interested in sequence number for syncing
        face_det_nn.passthrough.link(script.inputs['face_pass'])

        copy_manip.out.link(script.inputs['preview'])

        with open("script.py", "r") as f:
            script.setScript(f.read())

        print("Creating Head pose estimation NN")

        headpose_manip = pipeline.create(dai.node.ImageManip)
        headpose_manip.initialConfig.setResize(60, 60)
        headpose_manip.setWaitForConfigInput(True)
        script.outputs['manip_cfg'].link(headpose_manip.inputConfig)
        script.outputs['manip_img'].link(headpose_manip.inputImage)

        headpose_nn = pipeline.create(dai.node.NeuralNetwork)
        headpose_nn.setBlobPath(blobconverter.from_zoo(name="head-pose-estimation-adas-0001", shaves=6))
        headpose_manip.out.link(headpose_nn.input)

        headpose_nn.out.link(script.inputs['headpose_in'])
        headpose_nn.passthrough.link(script.inputs['headpose_pass'])

        print("Creating face recognition ImageManip/NN")

        face_rec_manip = pipeline.create(dai.node.ImageManip)
        face_rec_manip.initialConfig.setResize(112, 112)
        face_rec_manip.inputConfig.setWaitForMessage(True)

        script.outputs['manip2_cfg'].link(face_rec_manip.inputConfig)
        script.outputs['manip2_img'].link(face_rec_manip.inputImage)

        face_rec_nn = pipeline.create(dai.node.NeuralNetwork)
        face_rec_nn.setBlobPath(blobconverter.from_zoo(name="face-recognition-arcface-112x112", zoo_type="depthai", shaves=6))
        face_rec_manip.out.link(face_rec_nn.input)

        arc_xout = pipeline.create(dai.node.XLinkOut)
        arc_xout.setStreamName('recognition')
        face_rec_nn.out.link(arc_xout.input)
        



