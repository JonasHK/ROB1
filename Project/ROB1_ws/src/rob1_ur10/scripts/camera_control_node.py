#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import time
import rospy
import std_msgs.msg
from sensor_msgs.msg import Image
import numpy as np
from cv_bridge import CvBridge, CvBridgeError


cvb = CvBridge()


def msg_to_numpy(data):
    """Extracts image data from Image message.
    Args:
        data (sensor_msgs/Image): The ROS Image message, exactly as passed
            by the subscriber to its callback.
    Returns:
        The image, as a NumPy array.
    """
    return cvb.imgmsg_to_cv2(data, "bgr8")


def numpy_to_msg(img):
    """Builds a Image message from a NumPy array.
    Args:
        img (np.array): A NumPy array containing the RGB image data.
    Returns:
        A sensor_msgs/Image containing the image data.
    """
    return cvb.cv2_to_imgmsg(img, "bgr8")



stream_addr = 'http://192.168.0.20/video.cgi'
img_addr = 'http://192.168.0.20/image/jpeg.cgi'

# Select stream address instead of 0, when webcam is connected
cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture(stream_addr)



def camera_pub():
    print('Starting camera publisher nodes')
    # Define image publisher node
    rospy.init_node('image_cquisition', anonymous=True)
    pub = rospy.Publisher('camera_stream', Image, queue_size=10)

    # Set the publishing rate
    rate = rospy.Rate(1) # 5 Hz



    while not rospy.is_shutdown():
        # Read new frame
        ret, frame = cap.read()

        if not ret:
        	break

        # Convert frame to ROS message
        img_msg = numpy_to_msg(frame)

        # Publish frame
        pub.publish(img_msg)

        # Wait
        rate.sleep()



if __name__ == '__main__':
    try:
        camera_pub()
    except rospy.ROSInterruptException:
        pass
