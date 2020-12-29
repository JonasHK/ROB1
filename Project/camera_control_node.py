#!/usr/bin/env python3
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
	
	# Define image publisher node
    rospy.init_node('camera_pub', anonymous=True)
	pub = rospy.Publisher('camera_stream', Image, queue_size=10)
    
	# Set the publishing rate
    rate = rospy.Rate(5) # 5 Hz

    # img_msg = Image()
    # img_msg.header.stamp = time.time
    # img_msg.height = 480
    # img_msg.width = 640
    # img_msg.encoding = 'bgr8'
    # img_msg.is_bigendian = False
    # img_msg.step = 1920

	
    while not rospy.is_shutdown():
        # Read next frame
        ret, frame = cap.read()

        if not ret:
        	break
		
		# Convert frame to ROS message
		img_msg = numpy_to_msg(frame)
		
        # Publish frame
        # img_msg.data = frame
        pub.publish(img_msg)

        # Wait
        rate.sleep()



if __name__ == '__main__':
    try:
        camera_pub()
    except rospy.ROSInterruptException:
        pass
