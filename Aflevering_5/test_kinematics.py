# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 07:59:37 2020

@author: jonas
"""
import numpy as np
from UR10_invKin import UR10_invKin
from UR10_forKin import FrameTrans
from UR10_forKin import UR10_forKin


desired_pos = np.matrix([
[ 0.00, 0.87, -0.50,  0.36],
[-1.00, 0.00,  0.00, -0.11],
[ 0.00, 0.50,  0.87,  0.43],
[ 0.00, 0.00,  0.00,  1.00]])

qn = UR10_invKin(desired_pos)
print(qn)
print('--------------')

Desired_pose = UR10_forKin(qn,1)
print(Desired_pose)