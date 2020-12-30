#!/usr/bin/env python
import rospy
import numpy as np
import time
from rob1_ur10.srv import ImageProcessing, ImageProcessingResponse

def image_processing_client(x):
    rospy.wait_for_service('image_processing')
    try:
        imageProcessProxy = rospy.ServiceProxy('image_processing', ImageProcessing)
        resp1 = imageProcessProxy(x)
        return resp1
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

# def add_two_ints_client(x, y):
#     rospy.wait_for_service('add_two_ints')
#     try:
#         add_two_ints = rospy.ServiceProxy('add_two_ints', AddTwoInts)
#         resp1 = add_two_ints(x, y)
#         return resp1.sum
#     except rospy.ServiceException as e:
#         print("Service call failed: %s"%e)

if __name__ == '__main__':
    client_answer = image_processing_client(1)
    print('x center offset')
    print(client_answer.x_center_offset)
    print('y center offset')
    print(client_answer.y_center_offset)
