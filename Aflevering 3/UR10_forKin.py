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
#from UR10_invKin import UR10_invKin

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


from UR10_forKin import FrameTrans

# Parameters
global d1, a2, a3, a7, d4, d5, d6
tool_length = 0.15 # [m]
d1 =  0.1273
a2 = -0.612
a3 = -0.5723
a7 =  0.075
d4 =  0.163941
d5 =  0.1157
d6 =  0.0922 + tool_length

d = mat([d1, 0, 0, d4, d5, d6])
a = mat([0 , a2, a3, 0, 0, 0])

alph = mat([pi/2, 0, 0, pi/2, -pi/2, 0 ])

def UR10_invKin(desired_pos):# T60
  th = mat(np.zeros((6, 8)))
  P_05 = (desired_pos * mat([0,0, -d6, 1]).T-mat([0,0,0,1 ]).T)
  
  # **** theta1 ****
  
  psi = atan2(P_05[2-1,0], P_05[1-1,0])
  phi = acos(d4 /sqrt(P_05[2-1,0]*P_05[2-1,0] + P_05[1-1,0]*P_05[1-1,0]))
  #The two solutions for theta1 correspond to the shoulder
  #being either left or right
  th[0, 0:4] = pi/2 + psi + phi
  th[0, 4:8] = pi/2 + psi - phi
  th = th.real
  
  # **** theta5 ****
  
  cl = [0, 4]# wrist up or down
  for i in range(0,len(cl)):
	      c = cl[i]
	      T_10 = linalg.inv(FrameTrans(1,th,c))
	      T_16 = T_10 * desired_pos
	      th[4, c:c+2] = + acos((T_16[2,3]-d4)/d6);
	      th[4, c+2:c+4] = - acos((T_16[2,3]-d4)/d6);

  th = th.real
  
  # **** theta6 ****
  # theta6 is not well-defined when sin(theta5) = 0 or when T16(1,3), T16(2,3) = 0.

  cl = [0, 2, 4, 6]
  for i in range(0,len(cl)):
	      c = cl[i]
	      T_10 = linalg.inv(FrameTrans(1,th,c))
	      T_16 = linalg.inv( T_10 * desired_pos )
	      th[5, c:c+2] = atan2((-T_16[1,2]/sin(th[4, c])),(T_16[0,2]/sin(th[4, c])))
		  
  th = th.real

  # **** theta3 ****
  cl = [0, 2, 4, 6]
  for i in range(0,len(cl)):
	      c = cl[i]
	      T_10 = linalg.inv(FrameTrans(1,th,c))
	      T_65 = FrameTrans( 6,th,c)
	      T_54 = FrameTrans( 5,th,c)
	      T_14 = ( T_10 * desired_pos) * linalg.inv(T_54 * T_65)
	      P_13 = T_14 * mat([0, -d4, 0, 1]).T - mat([0,0,0,1]).T
	      t3 = cmath.acos((linalg.norm(P_13)**2 - a2**2 - a3**2 )/(2 * a2 * a3)) # norm ?
	      th[2, c] = t3.real
	      th[2, c+1] = -t3.real

  # **** theta2 and theta 4 ****

  cl = [0, 1, 2, 3, 4, 5, 6, 7]
  for i in range(0,len(cl)):
	      c = cl[i]
	      T_10 = linalg.inv(FrameTrans( 1,th,c ))
	      T_65 = linalg.inv(FrameTrans( 6,th,c))
	      T_54 = linalg.inv(FrameTrans( 5,th,c))
	      T_14 = (T_10 * desired_pos) * T_65 * T_54
	      P_13 = T_14 * mat([0, -d4, 0, 1]).T - mat([0,0,0,1]).T
	      
	      # theta 2
	      th[1, c] = -atan2(P_13[1], -P_13[0]) + asin(a3* sin(th[2,c])/linalg.norm(P_13))
	      # theta 4
	      T_32 = linalg.inv(FrameTrans( 3,th,c))
	      T_21 = linalg.inv(FrameTrans( 2,th,c))
	      T_34 = T_32 * T_21 * T_14
	      th[3, c] = atan2(T_34[1,0], T_34[0,0])
  th = th.real

  return th


if __name__ == "__main__":
    qn = np.matrix([[-1.574517552052633],
                    [-2.702589813862936],
                    [-1.477959934865133],
                    [-0.45558482805360967],
                    [2.1746609210968018],
                    [-2.12541371980776]])  
    qndeg = np.rad2deg(qn)
    
    print(qndeg)
    
    c = [0]
        
    o = UR10_forKin(qn,c)
    print(o)
    #qn =UR10_invKin(o)
    #print(qn)
