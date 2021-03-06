#!/usr/bin/env python
from moveTo import initMove moveToPose
import numpy as np
import time
from translate import translate


# Defines
move_ratio = 0.75       # Ratio of distance to block the robot moves per iteration
goal_tolerance = 0.02   # [m] Acceptable horizontal distance to block
delay = 30              # [s] Delay between new image, when the fov is empty

initPos = np.matrix(
[[-0.15950243,  0.9870943,  -0.01427658,  0.13134775],
 [ 0.98016869,  0.16007287,  0.11681614, -0.58283271],
 [ 0.11759384,  0.004639,   -0.99305094,  0.13799711],
 [ 0.,          0.,          0.,          1.        ]])
blue_bin_coor = np.matrix(
[[-0.15950243,  0.9870943,  -0.01427658,  -0.6],
 [ 0.98016869,  0.16007287,  0.11681614, -0.6],
 [ 0.11759384,  0.004639,   -0.99305094,  0.14],
 [ 0.,          0.,          0.,          1.        ]])
red_bin_coor = np.matrix(
[[-0.15950243,  0.9870943,  -0.01427658,  0.6],
 [ 0.98016869,  0.16007287,  0.11681614,  0.6],
 [ 0.11759384,  0.004639,   -0.99305094,  0.14],
 [ 0.,          0.,          0.,          1.        ]])



def image_processing_client(x):
    rospy.wait_for_service('image_processing')
    try:
        imageProcessProxy = rospy.ServiceProxy('image_processing', srvType)
        resp1 = imageProcessProxy(x)
        return resp1
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

def rotate_to_align(robot_pose,ang):
    next_point = np.copy(robot_pose)
    rotz = np.matrix(
    [[ cos(ang), -sin(ang), 0., 0.],
     [ sin(ang),  cos(ang), 0., 0.],
     [ 0.,       0.,        1., 0.],
     [ 0.,       0.,        0., 1.]])   # Rotation matrix along the z-axis
    next_point = next_point*rotz
    return next_point

# def block_in_robot_coor()
    

# Initiate the MoveUR node
initMove()

# Move to starting position.
moveToPose(initPos,20.0)

while 1:
    # Call image processing service to get movement coordinates
    img_coor = image_processing_client(1)
    block_color = img_coor.color
    
    # Open gripper
    
    while block_color not 0:
        block_dist = np.linalg.norm(img_coor.x_center_offset,img_coor.y_center_offset)
        # Move above a block to be picked up
        while block_dist > goal_tolerance:
    
            x_move = img_coor.x_center_offset * move_ratio
            y_move = img_coor.y_center_offset * move_ratio
    
            # Move towards target
            newPos = translate(initPos, x_move, y_move, 0.0)
            print('Move above target')
            moveToPose(newPos, 2.5)
            # Request for new coordinates to block
            img_coor = image_processing_client(1)
    
        # Perform coordinate frame transformation on the block's pose from camera to
        # robot
        # block_in_robot_coor()
    
        # Move and rotate the robot's tool to be above and aligned with the block_dist
        angle_rotation = img_coor.angle_offset
        next_pose = rotate_to_align(newPos,angle_rotation)
        moveToPose(next_pose,5.0)
    
        # Move down
        newPos = translate(newPos, 0.0, 0.0, -0.65)
        print('Move down')
        moveToPose(newPos, 8.0)
      
        # Close gripper 
    
        # Move up
        newPos = translate(newPos, 0.0, 0.0, 0.65)
        print(newPos)
        print('Move up')
        moveToPose(newPos, 8.0)
    
        # Move to position above storage box
        if color == 1:
            print('Move to position above blue storage box')
            endPos = blue_bin_coor
        elif color == 2:
            print('Move to position above red storage box')
            endPos = red_bin_coor
        moveToPose(endPos, 11)
    
        # Move down in storage box
        newPos = translate(endPos, 0.0, 0.0, -0.6)
        print('Move down in storage box')
        moveToPose(newPos, 8.0)
    
        # Open gripper
    
        # Move out of storage box again
        print('Move out of storage box')
        moveToPose(endPos, 8.0)
    
        # Move back to start
        moveToPose(initPos,13.0)
        print('Move back to start position again')
        print(initPos)
    
        img_coor = image_processing_client(1)
        block_color = img_coor.color
    
    time.sleep(delay)