import numpy as np


def invkin(xyz):
    """
    Python implementation of the the inverse kinematics for the crustcrawler
    Input: xyz position
    Output: Angels for each joint: q1,q2,q3,q4
    
    You might adjust parameters (d1,a1,a2,d4).
    The robot model shown in rviz can be adjusted accordingly by editing au_crustcrawler_ax12.urdf
    """
    d1 = 12.0; # cm (height of 2nd joint)
    a1 = 62.0; # (distance along "y-axis" to 2nd joint)
    a2 = 58.0; # (distance between 2nd and 3rd joints)
    d4 = 13.0; # (distance from 3rd joint to gripper center - all inclusive, ie. also 4th joint)
    


    #% Calculate oc
    #oc = 
    xc = xyz[0]
    yc = xyz[1]
    zc = xyz[2]
    
    
    #% Calculate q1
    q1 = np.arctan2(yc, xc)
    
    
    #% Calculate q2 and q3
    r2 = (xc - a1*np.cos(q1))**2 + (yc - a1*np.sin(q1))**2
    s = (zc - d1)
    D = ( r2 + s**2 - a2**2 - d4**2)/(2*a2*d4)
    
    q3 = np.arctan2(-np.sqrt(1-D**2), D)
    q2 = np.arctan2(s, np.sqrt(r2)) - np.arctan2(d4*np.sin(q3), a2 + d4*np.cos(q3))
    
    
    #% calculate q4 - ie. rotation part
    q4 = 0
    
    return q1,q2,q3,q4