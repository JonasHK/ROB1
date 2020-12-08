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

print('Start Position')
print(initPos)
#moveTo(initPos,20.0)
moveTo(initPos,5.0)

# Move above target
newPos = translate(initPos, 0.20, 0.1, 0.0)
print('Move above target')
moveTo(newPos, 2.5)

# Move down
newPos = translate(newPos, 0.0, 0.0, -0.65)
print(newPos)
print('Move down')
moveTo(newPos, 8.0)



# Open gripper


# Move towards object
newPos = translate(newPos, 0.0, -0.05, 0.0)
print(newPos)
print('Move towards object')
moveTo(newPos, 2.0)


# Close gripper



# Move up
newPos = translate(newPos, 0.0, 0.0, 0.65)
print(newPos)
print('Move up')
moveTo(newPos, 8.0)


# Move to position above storage box
endPos = np.matrix(
[[-0.15950243,  0.9870943,  -0.01427658,  -0.6],
 [ 0.98016869,  0.16007287,  0.11681614, -0.6],
 [ 0.11759384,  0.004639,   -0.99305094,  0.14],
 [ 0.,          0.,          0.,          1.        ]])
print('Move to position above storage box')
moveTo(endPos, 11)


# Move down in storage box
newPos = translate(endPos, 0.0, 0.0, -0.6)
print(newPos)
print('Move down in storage box')
moveTo(newPos, 8.0)

# Open gripper


# Move back to start
initPos = np.matrix(
[[-0.15950243,  0.9870943,  -0.01427658,  0.13134775],
 [ 0.98016869,  0.16007287,  0.11681614, -0.58283271],
 [ 0.11759384,  0.004639,   -0.99305094,  0.13799711],
 [ 0.,          0.,          0.,          1.        ]])
moveTo(initPos,13.0)
print('Move back to start position again')
print(initPos)


