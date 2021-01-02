#!/usr/bin/env python
from __future__ import print_function
import time
import roslib; roslib.load_manifest('ur_driver')
import rospy
import actionlib
from control_msgs.msg import *
from trajectory_msgs.msg import *

import numpy as np
from UR10_invKin import UR10_invKin
from UR10_forKin import FrameTrans
from UR10_forKin import UR10_forKin
from math import pi

JOINT_NAMES = ['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint',
               'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']

def moveToPose(des_pose,time):
    # Convert pose to joint angles
    qn1 = UR10_invKin(des_pose)
    # Find the first elbow-up configuration
    config = 0
    for index in range(0,8):
        if qn1[3,index] > 0 and qn1[2,index] > -pi/2 and qn1[2,index] < pi/2:
            config = index
            break

    Q1 = qn1[:,config]

    # Create goal message
    g = FollowJointTrajectoryGoal()
    g.trajectory = JointTrajectory()
    g.trajectory.joint_names = JOINT_NAMES
    g.trajectory.points = [
        JointTrajectoryPoint(positions=Q1, velocities=[0]*6, time_from_start=rospy.Duration(time))]

    # Publish goal message using actionlib
    client.send_goal(g)

    try:
        client.wait_for_result()
    except KeyboardInterrupt:
        client.cancel_goal()
        raise

def initMove():
    global client
    try:
        rospy.init_node("MoveUR", anonymous=True, disable_signals=True)
        client = actionlib.SimpleActionClient('follow_joint_trajectory', FollowJointTrajectoryAction)
        print("Waiting for server...")
        client.wait_for_server()
        print("Connected to server")
    except KeyboardInterrupt:
        rospy.signal_shutdown("KeyboardInterrupt")
        raise
