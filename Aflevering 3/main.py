#!/usr/bin/env python
from moveTo import moveTo
import numpy as np
from translate import translate


# Move to starting position.
initPos = np.matrix(
[[-0.15950243,  0.9870943,  -0.01427658,  0.13134775],
 [ 0.98016869,  0.16007287,  0.11681614, -0.58283271],
 [ 0.11759384,  0.004639,   -0.99305094,  0.13799711],
 [ 0.,          0.,          0.,          1.        ]])

#moveTo(initPos,4.0)

newPos = translate(initPos, 0.1, 0.1, 0.0)

print(newPos)

#for i in range(10):
	


# Camera Operation




# Move to new
