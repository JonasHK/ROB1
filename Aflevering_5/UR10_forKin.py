# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 20:10:05 2020

@author: jonas
"""
import numpy as np
from numpy import linalg


import cmath
import math
from math import cos as cos
from math import sin as sin
from math import atan2 as atan2
from math import acos as acos
from math import asin as asin
from math import sqrt as sqrt
from math import pi as pi

global mat
mat=np.matrix

# Parameters
d = mat([0.1273, 0, 0, 0.163941, 0.1157, 0.0922])
a =mat([0 ,-0.612 ,-0.5723 ,0 ,0 ,0])

alph = mat([pi/2, 0, 0, pi/2, -pi/2, 0 ])

def FrameTrans( n,qn,c  ):

  T_a = mat(np.identity(4), copy=False)
  T_a[0,3] = a[0,n-1]
  T_d = mat(np.identity(4), copy=False)
  T_d[2,3] = d[0,n-1]

  Rzt = mat([[cos(qn[n-1,c]), -sin(qn[n-1,c]), 0 ,0],
	         [sin(qn[n-1,c]),  cos(qn[n-1,c]), 0, 0],
	         [0,               0,              1, 0],
	         [0,               0,              0, 1]],copy=False)
      

  Rxa = mat([[1, 0,                 0,                  0],
			 [0, cos(alph[0,n-1]), -sin(alph[0,n-1]),   0],
			 [0, sin(alph[0,n-1]),  cos(alph[0,n-1]),   0],
			 [0, 0,                 0,                  1]],copy=False)

  A_i = T_d * Rzt * T_a * Rxa
	    

  return A_i

def UR10_forKin(qn,c ):  
  A_1=FrameTrans( 1,qn,c  )
  A_2=FrameTrans( 2,qn,c  )
  A_3=FrameTrans( 3,qn,c  )
  A_4=FrameTrans( 4,qn,c  )
  A_5=FrameTrans( 5,qn,c  )
  A_6=FrameTrans( 6,qn,c  )
      
  T_06=A_1*A_2*A_3*A_4*A_5*A_6

  return T_06

#qn = np.matrix([[np.radians(0.0)],
#                [np.radians(180.0)],
#                [np.radians(90.0)],
#                [np.radians(40.0)],
#                [np.radians(90.0)],
 #               [np.radians(0.0)]])
#c = [0]
    
#o = UR10_forKin(qn,c)
#print(o)