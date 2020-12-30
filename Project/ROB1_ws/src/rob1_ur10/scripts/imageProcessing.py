#!/usr/bin/env python
# ROS Node
from __future__ import print_function
from rob1_ur10.srv import ImageProcessing, ImageProcessingResponse
import rospy
import cv2
import time
from sensor_msgs.msg import Image
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
import matplotlib.pyplot as plt

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



class ImageSubscriber:
    def __init__(self):
        self.name = 'kurt'

    def image_callback(self,data):
        print('Image received')
        np_image = msg_to_numpy(data)
        self.np_image = np_image
        # # Display received image to show connection
        # cv2.imshow(winname = 'received_image', mat=self.get_np_image())
        # cv2.waitKey(30)

    def get_np_image(self):
        return self.np_image



def handle_image_processing(req):
    x_center_offset = 1
    y_center_offset = 2
    angle_offset = 3
    color = 4
    image_test = subscriber_obj.get_np_image()
    print(image_test)
    # cv2.imshow(winname = 'received_image', mat=image_test)
    # cv2.waitKey(30)
    plt.imshow(cv2.cvtColor(image_test, cv2.COLOR_BGR2RGB))
    plt.show()
    return ImageProcessingResponse(x_center_offset, y_center_offset, angle_offset, color)



def image_processing_server():
    rospy.init_node('image_processing_server')

    # Initialize camera subscriber
    global subscriber_obj
    subscriber_obj = ImageSubscriber()
    rospy.Subscriber("camera_stream", Image, subscriber_obj.image_callback)

    # Initialize Service
    s = rospy.Service('image_processing', ImageProcessing, handle_image_processing)


    rospy.spin()


if __name__ == "__main__":
    image_processing_server()
