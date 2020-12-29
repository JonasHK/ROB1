#!/usr/bin/env python
"""
Used to test functionality of camera_control_node.
"""
import cv2
import rospy
import time
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


def image_callback(data):
    print('Image received')
    np_image = msg_to_numpy(data)

    # Display received image to show connection
    cv2.imshow(winname = 'received_image', mat=np_image)
    cv2.waitKey(30)


def camera_sub():
    # Initialize camera subscriber node
    rospy.init_node('camera_sub', anonymous=True)
    rospy.Subscriber("camera_stream", Image, image_callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    camera_sub()
