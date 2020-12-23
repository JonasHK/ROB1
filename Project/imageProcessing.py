# ROS Node
from _future_ import print_function
from beginner_tutorials.srv import ImageProcessing, ImageProcessingResponse
import rospy

def handle_image_processing(req):
    x_center_offset = 1
    y_center_offset = 2
    angle_offset = 3
    color = 4
    return ImageProcessingResponse(x_center_offset, y_center_offset, angle_offset, color)

def image_processing_server():
    rospy.init_node('image_processing_server')
    s = rospy.Service('image_processing', ImageProcessing, handle_image_processing)
    rospy.spin()

if _name_ == "_main_":
    image_processing_server()
