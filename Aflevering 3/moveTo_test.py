#!/usr/bin/env python
from moveTo import moveTo
import numpy as np
desired_pos = np.matrix(
 [[-9.09244997e-04,  9.89964338e-01,  1.41314484e-01,  30.67272116e-02],
 [ 9.79651168e-01,  2.92444446e-02, -1.98565734e-01, -8.8008224e-01],
 [-2.00705659e-01,  1.38258355e-01, -9.69846310e-01,  24.33077441e-02],
 [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]])




#[[-0.73911612 -0.08837746 -0.66775504 -0.6448901 ]
# [ 0.21049999 -0.97200865 -0.10435007 -0.48171171]
# [-0.63984148 -0.21768925  0.73703072  1.05651164]
# [ 0.          0.          0.          1.        ]]



moveTo(desired_pos,4.0)