#!/usr/bin/env python
import rospy
import numpy as np
import matplotlib.pyplot as plt
import time
import cv2
from cv_bridge import CvBridge, CvBridgeError
from rob1_ur10.srv import ImageProcessing, ImageProcessingResponse

# Defines
request_delay = 2

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


def image_processing_client(x):
    rospy.wait_for_service('image_processing')
    try:
        imageProcessProxy = rospy.ServiceProxy('image_processing', ImageProcessing)
        resp1 = imageProcessProxy(x)
        return resp1
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

def show_image_data(client_answer, verbose):
    if verbose == 1:
        print('x center offset =' + str(client_answer.x_center_offset))
        print('y center offset = ' + str(client_answer.y_center_offset))
        print('Angle offset = ' + str(client_answer.angle_offset))
        print('Box color = ' + str(client_answer.color) + '\n')
    returned_img = msg_to_numpy(client_answer.image_object)
    plt.imshow(cv2.cvtColor(returned_img, cv2.COLOR_BGR2RGB))
    plt.show()


if __name__ == '__main__':
    # Make service requests
    client_answer1 = image_processing_client(1)
    time.sleep(request_delay)
    client_answer2 = image_processing_client(1)
    time.sleep(request_delay)
    client_answer3 = image_processing_client(1)
    time.sleep(request_delay)
    client_answer4 = image_processing_client(1)
    time.sleep(request_delay)
    client_answer5 = image_processing_client(1)
    time.sleep(request_delay)
    client_answer6 = image_processing_client(1)

    #Display result
    show_image_data(client_answer1, 1)
    show_image_data(client_answer2, 1)
    show_image_data(client_answer3, 1)
    show_image_data(client_answer4, 1)
    show_image_data(client_answer5, 1)
    show_image_data(client_answer6, 1)
