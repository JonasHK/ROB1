#!/usr/bin/env python
import numpy as np

def translate(point, x, y, z):
	nextPoint = np.copy(point)
	nextPoint[0,3] = x + nextPoint[0,3]
	nextPoint[1,3] = y + nextPoint[1,3]
	nextPoint[2,3] = z + nextPoint[2,3]

	return nextPoint
