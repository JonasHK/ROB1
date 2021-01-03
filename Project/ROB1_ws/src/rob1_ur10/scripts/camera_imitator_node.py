#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import os
import time
import rospy
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



def camera_imitator_pub():
    print('Starting camera imitating publisher nodes')
    # Define image publisher node
    rospy.init_node('camera_imitator_pub', anonymous=True)
    pub = rospy.Publisher('camera_stream', Image, queue_size=10)

    # Set the publishing rate
    rate = rospy.Rate(0.5)
    img_nr = 8


    while not rospy.is_shutdown():
        if img_nr == 14:
            img_nr = 8

        # Create absolute image path
        # absolute_path = os.path.join(os.getcwd(),'src', 'rob1_ur10', 'scripts', 'Figure_1.png');
        img_name = 'img_' + str(img_nr) + '.jpg'
        absolute_path = os.path.join(os.getcwd(),'src', 'rob1_ur10', 'scripts', img_name);

        # Read image
        img = cv2.imread(absolute_path)

        # Convert img to ROS message
        img_msg = numpy_to_msg(img)

        # Publish frame
        pub.publish(img_msg)

        img_nr = img_nr + 1

        # Wait
        rate.sleep()



if __name__ == '__main__':
    try:
        camera_imitator_pub()
    except rospy.ROSInterruptException:
        pass
