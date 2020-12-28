#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import time
import rospy
import std_msgs.msg
from sensor_msgs.msg import Image

# Disable user control in
# Go to http://192.168.0.20 and select maintanance


stream_addr = 'http://192.168.0.20/video.cgi'
#stream_addr = 'admin@http://192.168.0.20/video.cgi?.mjpg'
#stream_addr = '192.168.0.20/mjpeg.cgi'
img_addr = 'http://192.168.0.20/image/jpeg.cgi'

# Select stream address instead of 0, when webcam is connected
cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture(stream_addr)


# cv2.namedWindow('frame',cv2.WINDOW_NORMAL)
# while(cap.isOpened()):
    # t=time.time()
    # # Read next frame
    # ret, frame = cap.read()

    # if not ret:
        # break

    # # Show the frame
    # cv2.imshow('frame', frame)

    # print(frame.shape)
    # print(1 / (time.time()-t),'Hz')

    # if cv2.waitKey(1) & 0xFF == ord('q'):
        # break

#VidOut.release()

def camera_pub():
    pub = rospy.Publisher('camera_stream', Image, queue_size=10)
    rospy.init_node('camera_pub', anonymous=True)
    rate = rospy.Rate(5) # 5 Hz

    img_msg = Image()
    img_msg.header.stamp = time.time
    img_msg.height = 480
    img_msg.width = 640
    img_msg.encoding = 'bgr8'
    img_msg.is_bigendian = False
    img_msg.step = 1920


    while not rospy.is_shutdown():
        # Read next frame
        ret, frame = cap.read()

        if not ret:
        	break

        # Publish frame
        img_msg.data = frame
        pub.publish(img_msg)

        # Wait
        rate.sleep()



if __name__ == '__main__':
    try:
        camera_pub()
    except rospy.ROSInterruptException:
        pass
